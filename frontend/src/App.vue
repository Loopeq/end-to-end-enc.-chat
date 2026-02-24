<script setup lang="ts">

interface User {
  name: string
  email: string
}

const commonUser: User = {
  name: 'Hello World',
  email: 'admin@gmail.com'
}
</script>

<template>
  <div>{{ commonUser.name }}</div>
</template>

<style scoped>
</style>
