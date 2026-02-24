<script setup lang="ts">
import { ref } from 'vue'

const messages = ref<{ id: string; sender: string; text: string }[]>([])
</script>

<template>
<div class="chat-window">
    <div
    v-for="msg in messages"
    :key="msg.id"
    :class="['message', msg.sender === 'User' ? 'outgoing' : 'incoming']"
    >
    <strong v-if="msg.sender !== 'User'">{{ msg.sender }}: </strong>{{ msg.text }}
    </div>
</div>
</template>
  
<style lang="scss" scoped>

</style>