<template>

<div>

  <time-picker v-model:update="timer" />

 </div>

</template>
<script setup lang="ts">
import TimePicker from '@/components/layout/TimePicker.vue'
import { ref, watch } from 'vue'
const timer = ref()
watch(timer, (val) => {
  console.log(val)
})
</script>
