<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
 (e: "send", text: string): void
}>()

const text = ref('')

const send = () => {
    const message = text.value.trim()
    if (message === '') return
    emit('send', message)
    text.value = ''
}
</script>

<template>
    <div class="message-input">
        <input v-model="text" @keyup.enter="send" placeholder="Type a message" />
        <button @click="send">Send</button>
    </div>
</template>
  
<style lang="scss" scoped>

</style>