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
        <OnlineWindow :online="online"/>
      </aside>

      <main class="chat-area">
        <div class="chat-area-layout">
          <div class="messages-wrapper">
            <ChatWindow :messages="messages" />
          </div>
          <MessageInput @send="send" />
        </div>
      </main>

    </div>
  </div>
</template>

<style scoped>
.layout {
  max-height: calc(100vh - 100px) ;
}

.chat-layout {
  height: 100vh;
  display: grid;

  grid-template-columns: 260px 1fr;
  grid-template-rows: 60px 1fr 60px;

  grid-template-areas:
    "profile profile"
    "chatlist chat"
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
  height: 100%;
}

.chat-area-layout {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.messages-wrapper {
  flex: 1;
  overflow-y: auto;
}

</style>