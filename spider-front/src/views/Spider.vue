<template>
  <a-layout-content>
    <a-row>
      <a-col :md="24" :xs="24" :lg="12" class="p-sm">
        <a-card    style="min-height: 400px" title="输入配置项">
          <spider-config @spiderSuccess='spiderSuccess' @startSpider='startSpider'/>
        </a-card>
      </a-col>
      <a-col :md="24" :xs="24" :lg="12" class="p-sm">
        <spider-desc :response="response" :status="status"/>
      </a-col>
    </a-row>
  </a-layout-content>
</template>

<script lang="ts" setup>

import SpiderConfig from '@/components/spider/SpiderConfig.vue'
import SpiderDesc from '@/components/spider/SpiderDesc.vue'
import { ref } from 'vue'
import { spiderResponseOptionAble } from '@/core/spider/type'

const status = ref<boolean>(false)
/**
 * 响应
 * */
const response = ref<spiderResponseOptionAble>()

/**
 *开始调度任务时
 */
const startSpider = (): void => {
  status.value = true
}
/**
 *
 * 爬取完成
 */
const spiderSuccess = (data: spiderResponseOptionAble): void => {
  response.value = data
}
</script>

<style scoped>

</style>
