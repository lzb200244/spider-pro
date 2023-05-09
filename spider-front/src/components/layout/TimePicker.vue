<template>
  {{ timer }}
  <a-row>
    <a-col>
      <a-select
        ref="select"
        @select="handleChangeType"
        v-model:value="timer.type"
        @focus="focus">
        <a-select-option value="single">单 次</a-select-option>
        <a-select-option value="daily">周 期</a-select-option>
      </a-select>
    </a-col>
    <a-row v-if="timer.type==='single'">
      <a-date-picker value-format="YYYY-MM-DD HH:mm:ss"
                     format="YYYY-MM-DD HH:mm:ss"
                     :show-time="true" v-model:value="timer.timer.time"/>
    </a-row>
    <a-row v-else>
      <a-select style="width:auto" v-model:value="timer.type">
        <a-select-option value="daily">每 天</a-select-option>
        <a-select-option value="weekly">每 周</a-select-option>
      </a-select>
      <div>
        <a-row v-if="timer.type === 'daily'">
          <a-time-picker style="width:auto"
                         value-format="HH:mm"
                         format="HH:mm"
                         :show-time="true"
                         v-model:value="timer.timer.time"/>
        </a-row>
        <a-row v-else-if="timer.type === 'weekly'">
          <a-select style="width:auto" v-model:value="timer.timer.num">
            <template v-for="(k,i) in 7" :key="i">
              <a-select-option :value="i">周{{ i + 1 }}</a-select-option>
            </template>
          </a-select>
          <a-time-picker style="width:auto"
                         value-format="HH:mm"
                         format="HH:mm"
                         :show-time="true"
                         v-model:value="timer.timer.time"/>
        </a-row>
      </div>
    </a-row>
  </a-row>

</template>

<script setup lang="ts">
import { defineEmits, watch } from 'vue'

import { useTask } from '@/hooks/useTask'

const emit = defineEmits(['update:modelValue', 'update:taskType'])

const { timer } = useTask()

// 创建任务

const handleChangeType = () => {
  timer.timer.time = ''
  timer.timer.num = 0
}

/**
 *筛选器
 */

watch(timer, (val) => {
  emit('update:modelValue', val)
})

</script>
