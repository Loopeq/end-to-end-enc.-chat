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

let connection: WebSocket | null = null

const send = (message: string) => { 
  console.log(message)
  if (connection && connection.readyState === WebSocket.OPEN) {
    connection.send(message)
  }
}

const connectWS = () => {
  connection = new WebSocket("ws://localhost:8000/api/ws")

  connection.onopen = () => console.log("WS connected")
  
  connection.onmessage = (e) => {
    messages.value.push(JSON.parse(e.data))
  }

  connection.onclose = () => console.log("WS closed")
  connection.onerror = (err) => console.error("WS error", err)
}

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
  connection?.close()
}


onMounted(async() => { 
  await userme()
})

</script>

<template>
  <div id="app">
    <h1>Encrypted Chat</h1>
    <LoginWindow v-if="!user" @login="login"/>
    <ProfileWindow v-else :user="user" @logout="logout"/>
    <ChatWindow :messages="messages"/>
    <MessageInput @send="send"/>
  </div>
</template>