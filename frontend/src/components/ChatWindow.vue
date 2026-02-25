<script setup lang="ts">
import { Message } from '../type';

defineProps<{
    messages: Message[]
}>()
</script>

<template>
<div class="chat-window">
    <div
        v-for="(msg, index) in messages"
        :key="index"
    >
        <strong>{{ msg.username }}: </strong>
        <span>{{ msg.message }}</span>
    </div>
</div>
</template>
  
<style lang="scss" scoped>

</style>