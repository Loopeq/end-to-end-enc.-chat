<script setup lang="ts">
import ChatWindow from './components/ChatWindow.vue'
import MessageInput from './components/MessageInput.vue'
import LoginWindow from './components/LoginWindow.vue'
import ProfileWindow from './components/ProfileWindow.vue'

import api from './services/api'
import { onMounted, ref } from 'vue'
import { User } from './type'
import { useWebSocket } from './services/ws'
import OnlineWindow from './components/OnlineWindow.vue'

const user = ref<User | null>(null)

const {
  messages,
  online,
  connect,
  disconnect,
  send,
  clearMessages
} = useWebSocket()

const login = async (payload: User) => {
  try {
    const response = await api.post("/api/login", payload)
    user.value = response.data
    connect()
  } catch (err) { 
    if (err.response && err.response.data) {
      alert(err.response.data.detail)
    } else {
      console.error(err)
    }
  }
}

const userme = async () => {
  try {
    const response = await api.get("/api/me", { withCredentials: true })
    user.value = response.data
    connect()
  } catch {
    user.value = null
  }
}

const getMessages = async () => {
  try {
    const response = await api.get("/api/messages", { withCredentials: true })
    messages.value = response.data
    connect()
  } catch {
    messages.value = []
  }
}


const logout = async () => {
  await api.post("/api/logout", {}, { withCredentials: true })

  user.value = null
  clearMessages()
  disconnect()
}

onMounted(async() => {
  await userme() 
  await getMessages()
})
</script>

<template>
  <div class="layout" id="app">
    <LoginWindow v-if="!user" @login="login" />

    <div v-else class="chat-layout">
      
      <header class="profile-area">
        <ProfileWindow :user="user" @logout="logout" />
      </header>

      <aside class="chat-list-area">
        <OnlineWindow :online="online" :username="user.username"/>
      </aside>

      <main class="chat-area">
        <div class="chat-area-layout">
          <ChatWindow :messages="messages" :username="user.username" />
        </div>
        <MessageInput @send="send" />
      </main>

    </div>
  </div>
</template>

<style scoped>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

.chat-layout {
  display: grid;
  height: calc(100vh - 50px);

  grid-template-columns: 260px 1fr;
  grid-template-rows: 60px 1fr;

  grid-template-areas:
    "profile profile"
    "chatlist chat";
}

.profile-area {
  grid-area: profile;
  border-bottom: 1px solid #ccc;
}

.chat-list-area {
  grid-area: chatlist;
  border-right: 1px solid #ccc;
  overflow-y: auto;
}

.chat-area {
  grid-area: chat;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-area-layout {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

@media (max-width: 768px) {

.chat-layout {
  grid-template-columns: 1fr;
  grid-template-rows: 60px 1fr;

  grid-template-areas:
    "profile"
    "chat";
}

.chat-list-area {
  display: none;
}
}
</style>