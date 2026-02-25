<script setup lang="ts">
import { User } from "../type";

const emit = defineEmits<{
 (e: "logout"): void
}>()

const props = defineProps<{
    user: User
}>()

</script>

<template>
  <div>
    {{ user.username }}
    <button @click="emit('logout')">Выйти</button>
  </div>
</template>