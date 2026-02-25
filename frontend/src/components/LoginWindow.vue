<script setup lang="ts">
import { ref } from "vue";
import { User } from "../type";

const emit = defineEmits<{
 (e: "login", payload: User): void
}>()

const username = ref("");
const password = ref("");

const submit = async () => {
  emit('login', {
    username: username.value, 
    password: password.value
  })
};
</script>

<template>
  <div>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="submit">Login</button>
  </div>
</template>