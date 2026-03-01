<script setup lang="ts">
import { computed } from 'vue';
import { User } from '../type';


const props = defineProps<{
    online: User[]
    username: string
}>()

const emit = defineEmits<{
  (e: 'handshake', userId: string): void
}>()

const sortedOnline = computed(() => {
    return [...props.online].sort((a, b) => {
        if (a.username === props.username) return -1
        if (b.username === props.username) return 1
        return 0
    })
})

</script>

<template>
<div>
    Сейчас онлайн
    <div
        class="online-list"
        v-for="(user, index) in sortedOnline"
        @click="emit('handshake', user.id)"
        :key="index"
        :class="{ 'online-list-userme': user.username === username}"
    >
        <span class="online-list-dot">🟢</span><span class="online-list-username">{{ user.username }}</span>
    </div>
</div>
</template>
  
<style scoped>
.online-list{
    padding: 5px;
}
.online-list-dot{
    font-size: 10px;
    margin-right: 5px;
}

.online-list-userme::after{
    content: 'Вы'
}

.online-list-userme .online-list-username { 
    display: none;
}


</style>