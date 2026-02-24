<script setup lang="ts">
import { ref } from "vue";
import { useAuth } from "../services/useAuth";

const { user, login, error } = useAuth();
const username = ref("");
const password = ref("");

const submit = async () => {
  const ok = await login(username.value, password.value);
  if (ok) alert(`Welcome ${user.value?.username}`);
  else alert(`Error: ${error.value}`);
};
</script>

<template>
  <div>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="submit">Login</button>
  </div>
</template>