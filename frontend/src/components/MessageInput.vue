<script setup lang="ts">
    import { ref } from 'vue'

    const text = ref('')

    const sendMessage = () => {
        if (text.value.trim() === '') return
        text.value = '' 
    }
</script>

<template>
    <div class="message-input">
        <input v-model="text" @keyup.enter="sendMessage" placeholder="Type a message" />
        <button @click="sendMessage">Send</button>
    </div>
</template>
  
<style lang="scss" scoped>

</style>