<template>

  <div>
    <a-radio-group v-model:value="chart">
      <a-radio-button value="bar">柱状图</a-radio-button>
      <a-radio-button value="line">折线图</a-radio-button>
      <a-radio-button value="pie">饼图</a-radio-button>
    </a-radio-group>
  </div>
  <div ref="chartDom" style="width: auto;height: 450px">
  </div>

</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import useEcharts from '@/hooks/useEcharts'
const chartDom = ref()
const chart = ref<'bar' | 'line' | 'pie'>('bar')
const props = defineProps(['chart'])

const { chartOpt, initEcharts } = useEcharts(chartDom,
  props?.chart
)
// 初始化echarts
onMounted(() => {
  initEcharts()
})
// 切换
watch(chart, (value) => {
  chartOpt[value]()
  initEcharts()
})
</script>

<style scoped>

</style>
