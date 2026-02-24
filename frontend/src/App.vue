<script setup lang="ts">
import ChatWindow from './components/ChatWindow.vue'
import MessageInput from './components/MessageInput.vue'
import LoginWindow from './components/LoginWindow.vue';

</script>

<template>
  <div id="app">
    <h1>Encrypted Chat</h1>
    <LoginWindow />
    <ChatWindow />
    <MessageInput />
  </div>
</template>