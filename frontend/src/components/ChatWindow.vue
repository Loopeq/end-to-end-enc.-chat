<script setup lang="ts">
import { onUpdated, ref } from 'vue';
import { Conversation, Message } from '../type';

defineProps<{
    messages: Message[]
    conversation: Conversation | null
    me_id: string
}>()

const chatContainer = ref<HTMLElement | null>(null);

onUpdated(() => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
})

</script>

<template>
<div v-if="conversation" class="chat-window-partner">{{ conversation.partner.username }}</div>
<div v-else>Выберите собеседника слева</div>
<div class="chat-window" ref="chatContainer">
    <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="{ 'chat-window-userme': msg.from === me_id,
                  'chat-window-other': msg.from !== me_id
         }"
        >
        <span>{{ msg.message }}</span>
    </div>
</div>
</template>


<style>

.chat-window {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: auto;
  padding: 10px;
}

.chat-window-partner { 
  width: 100%;
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