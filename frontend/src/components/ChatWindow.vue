<script setup lang="ts">
import { Message } from '../type';

defineProps<{
    messages: Message[]
}>()
</script>

<template>
<div>
    <div
        v-for="(msg, index) in messages"
        :key="index"
    >
        <strong>{{ msg.username }}: </strong>
        <span>{{ msg.message }}</span>
    </div>
</div>
</template>