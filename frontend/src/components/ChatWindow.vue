<script setup lang="ts">
import { onUpdated, ref } from 'vue';
import { Message } from '../type';

defineProps<{
    messages: Message[]
    username: string
}>()

const chatContainer = ref<HTMLElement | null>(null);

onUpdated(() => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
})

</script>

<template>
<div class="chat-window" ref="chatContainer">
    <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="{ 'chat-window-userme': msg.username === username,
                  'chat-window-other': msg.username !== username
         }"
        >
        <strong v-if="msg.username !== username">{{ msg.username }}: </strong>
        <span>{{ msg.message }}</span>
    </div>
</div>
</template>


<style>

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: auto;
  padding: 10px;
}

.chat-window-userme {
  align-self: flex-end;
  background-color: #dcf8c6;
  padding: 8px 12px;
  border-radius: 12px;
  margin: 2px 0;
  max-width: 70%;
  word-break: break-word;
}

.chat-window-other {
  align-self: flex-start;
  background-color: #f1f0f0;
  padding: 8px 12px;
  border-radius: 12px;
  margin: 2px 0;
  max-width: 70%;
  word-break: break-word;
}
</style>