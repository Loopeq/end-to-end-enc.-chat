<script setup lang="ts">
import ChatWindow from './components/ChatWindow.vue'
import MessageInput from './components/MessageInput.vue'
import LoginWindow from './components/LoginWindow.vue';
import api from './services/api';
import { onMounted, ref } from 'vue';
import { Message, User } from './type';
import ProfileWindow from './components/ProfileWindow.vue';

const user = ref<User | null>(null)
const messages = ref<Message[]>([])

let ws: WebSocket | null = null;
let reconnectAttempts = 0;

const send = (message: string) => { 
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(message)
  }
}

const connectWS = () => {
  if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
    return;
  }

  ws = new WebSocket("ws://localhost:8000/api/ws");

  ws.onopen = () => {
    reconnectAttempts = 0;
  };

  ws.onmessage = (e) => {
    messages.value.push(JSON.parse(e.data));
  };

  ws.onclose = () => {
    const timeout = Math.min(30000, Math.pow(2, reconnectAttempts) * 500);
    reconnectAttempts++;
    setTimeout(connectWS, timeout);
  };

  ws.onerror = (err) => {
    console.error("WS error", err);
    ws?.close();
  };
};

const login = async (payload: User) => { 
  const response = await api.post("/api/login", payload)
  user.value = response.data;
  connectWS()
}

const userme = async () => { 
  const response = await api.get("/api/me", {withCredentials: true})
  user.value = response.data
  connectWS()
}

const logout = async () => {
  await api.post("/api/logout", {withCredentials: true})
  user.value = null;
  messages.value = [];
  ws?.close()
}


onMounted(async() => { 
  await userme()
})

</script>

<template>
  <div id="app">
    <LoginWindow v-if="!user" @login="login"/>
    <ProfileWindow v-else :user="user" @logout="logout"/>
    <ChatWindow :messages="messages"/>
    <MessageInput @send="send"/>
  </div>
</template>