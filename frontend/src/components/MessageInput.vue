<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import EmojiPicker from 'vue3-emoji-picker'

defineProps<{
    disabled: boolean
}>()

const emit = defineEmits<{
 (e: "send", text: string): void
}>()

const text = ref('')
const showPicker = ref(false);
const pickerRef = ref<HTMLElement | null>(null)

const send = () => {
    const message = text.value.trim()
    if (message === '') return
    emit('send', message)
    text.value = ''
}

const addEmoji = (emoji: any) => {
    text.value += emoji.i;
    showPicker.value = false;
};

const openEmoji = () => {
    showPicker.value = !showPicker.value
}


const handleClickOutside = (e: MouseEvent) => {
  if (!pickerRef.value) return

  if (!pickerRef.value.contains(e.target as Node)) {
    showPicker.value = false
  }
}


onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

</script>

<template>
    <div v-if="!disabled" class="message-input">
        <input v-model="text" @keyup.enter="send" placeholder="Печатать сообщение" class="message-input-field" />
        <button @click="send">Отправить</button>
        <button @click.stop="openEmoji">
            <span>😁</span>
            <div v-if="showPicker" ref="pickerRef">
                <EmojiPicker class="message-input-emoji" :native="true" @select="addEmoji" />
            </div>
        </button>
    </div>
</template>
  
<style scoped>
.message-input{ 
    height: 30px;
    width: 100%;
    position: relative;
    display: flex;
    flex-shrink: 0;
}

.message-input-field{
    width: 100%;
}

.message-input-emoji{
    position: absolute;
    bottom: 40px;
    right: 0;
}
</style>