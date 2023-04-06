<template>
  <a-layout-content>
    <a-row>
      <a-col :md="24" :xs="24" :lg="12" class="p-sm">
        <a-card style="min-height: 400px" title="输入配置项">
          <spider-config
            @spiderFailed="spiderFailed"
            @spiderSuccess='spiderSuccess'
            @startSpider='startSpider'/>
        </a-card>
      </a-col>
      <a-col :md="24" :xs="24" :lg="12" class="p-sm">
        <a-card title="爬取结果" style="min-height: 400px">

          <el-row v-if="loading">
            <div class="example">
              <a-spin />
            </div>
          </el-row>
          <el-row v-else>
            <template v-if="!success">
              <spider-desc v-model:response="response"/>
            </template>
            <template v-else>
              <a-empty/>
            </template>

          </el-row>

        </a-card>
      </a-col>
    </a-row>
  </a-layout-content>
</template>

<script lang="ts" setup>

import SpiderConfig from '@/components/spider/SpiderConfig.vue'
import SpiderDesc from '@/components/spider/SpiderDesc.vue'
import { ref } from 'vue'
import { SpiderResponseOptionAble } from '@/core/spider/type'

const loading = ref<boolean>(false)
const success = ref<boolean>(true)
/**
 * 响应
 * */
const response = ref<SpiderResponseOptionAble>()

/**
 *开始调度任务时
 */
const startSpider = (): void => {
  loading.value = true
}
/**
 *
 * 爬取完成
 */

const spiderSuccess = (data: SpiderResponseOptionAble): void => {
  loading.value = false
  success.value = false
  response.value = data
}
const spiderFailed = (): void => {
  loading.value = false
  success.value = true
}
</script>

<style scoped>
.example {
  text-align: center;
  border-radius: 4px;
  margin: 150px 0;
}
</style>
