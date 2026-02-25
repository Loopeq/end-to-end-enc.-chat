<script setup lang="ts">
import { ref } from 'vue'
import EmojiPicker from 'vue3-emoji-picker'

const emit = defineEmits<{
 (e: "send", text: string): void
}>()

const text = ref('')
const showPicker = ref(false);

const send = () => {
    const message = text.value.trim()
    if (message === '') return
    emit('send', message)
    text.value = ''
}

const addEmoji = (emoji: any) => {
    text.value += emoji.i;
    showPicker.value = false;
};

</script>

<template>
    <div class="message-input">
        <input v-model="text" @keyup.enter="send" placeholder="Type a message" />
        <span>
            <button @click="send">Send</button>
        </span>
    </div>
    <EmojiPicker :native="true" @select="addEmoji" />
</template>
  
<style lang="scss" scoped>

</style>