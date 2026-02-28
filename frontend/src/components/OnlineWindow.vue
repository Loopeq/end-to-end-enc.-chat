<script setup lang="ts">
import { ref } from 'vue';
import { Online } from '../type';

defineProps<{
    online: Online[]
}>()

const text = ref('')

const send = () => {
    console.log(text.value)
}

</script>

<template>
<div>
    Сейчас онлайн
    <div
        class="online-list"
        v-for="(msg, index) in online"
        :key="index"
    >
        <span class="online-list-dot">🟢</span><span> {{ msg }}</span>
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
</style>