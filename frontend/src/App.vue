<script setup lang="ts">
import ChatWindow from './components/ChatWindow.vue'
import MessageInput from './components/MessageInput.vue'
import LoginWindow from './components/LoginWindow.vue';
import api from './services/api';
import { onMounted, ref } from 'vue';
import { User } from './type';
import ProfileWindow from './components/ProfileWindow.vue';

const user = ref<User | null>(null);

const login = async (payload: User) => { 
  const response = await api.post("/api/login", payload)
  user.value = response.data;
}

const userme = async () => { 
  const response = await api.get("/api/me", {withCredentials: true})
  user.value = response.data
}

const logout = async () => {
  await api.post("/api/logout", {withCredentials: true})
  user.value = null;
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
    <ChatWindow />
    <MessageInput />
  </div>
</template>