<script setup lang="ts">
import { computed } from 'vue';


const props = defineProps<{
    online: string[]
    username: string
}>()

const sortedOnline = computed(() => {
    return [...props.online].sort((a, b) => {
        if (a === props.username) return -1
        if (b === props.username) return 1
        return 0
    })
})

</script>

<template>
<div>
    Сейчас онлайн
    <div
        class="online-list"
        v-for="(msg, index) in sortedOnline"
        :key="index"
        :class="{ 'online-list-userme': msg === username}"
    >
        <span class="online-list-dot">🟢</span><span class="online-list-username">{{ msg }}</span>
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