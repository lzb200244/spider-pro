<template>

  <el-row>
    <div>
      <a-modal v-model:visible="visible" title="输入下载文件名称" @ok="downLoadData">
        <a-input v-model="fileName"></a-input>
      </a-modal>
    </div>
    <el-loc>
      <template v-for="item in Object.keys(response||{})" :key="item">
        <a-card :title="optMap.get(item)" :bordered="false">
          <template v-if="item==='domain'">
            <a-descriptions
              class="font-600"
              :column="{  xl: 2, lg: 2, md: 2, sm: 2, xs: 1 }">
              <a-descriptions-item label="域名地址">{{ response.domain.domain_name }}</a-descriptions-item>
              <a-descriptions-item label="域名注册服务器">{{ response.domain.registrar }}</a-descriptions-item>
              <a-descriptions-item label="注册时间">{{ response.domain.creation_date }}</a-descriptions-item>
              <a-descriptions-item label="过期时间">{{ response.domain.expiration_date }}</a-descriptions-item>
              <a-descriptions-item label="注册邮箱">{{ response.domain.emails }}</a-descriptions-item>
              <a-descriptions-item label="户主">{{ response.domain.name }}</a-descriptions-item>
            </a-descriptions>
          </template>
          <template v-else-if="item==='text'">
            <a-skeleton :loading="false" :paragraph="{ rows: 10 }" active>
              <a-typography-paragraph>
                {{response?.text}}
              </a-typography-paragraph>
            </a-skeleton>
          </template>
          <template v-else-if="item==='imgList'">
            <template v-if="response.imgList?.length!==0">
              <img-load :imgList="response.imgList"/>
            </template>
          </template>
          <template v-else-if="item==='chart'">

          </template>
          <template v-else-if="item==='table' && response?.table">
            <charts :chart="response.chart"/>
            <a-button type="primary" @click="visible = true">下载表格</a-button>
            <a-table id="table" :dataSource="response?.table?.data" :scroll="{ x: 1500, y: 300 }"
                     :columns="response?.table?.columns"/>

          </template>
        </a-card>
      </template>
      <!--空对象-->
    </el-loc>
  </el-row>

</template>

<script lang="ts" setup>

import { SpiderResponseOptionAble } from '@/core/spider/type'
import { defineAsyncComponent, ref } from 'vue'
import useExcel from '@/hooks/useExcel'
// import Charts from '@/components/layout/Charts.vue'

interface Props {
  response: SpiderResponseOptionAble;
}

const ImgLoad = defineAsyncComponent(() => import('@/components/layout/ImgLoad.vue'))
const Charts = defineAsyncComponent(() => import('@/components/layout/Charts.vue'))
// eslint-disable-next-line vue/no-setup-props-destructure
const { response } = defineProps<Props>()
const visible = ref<boolean>(false)
const fileName = ref('test')
const loading = ref(true)

// 映射关系

const optMap = new Map<string, boolean>([
  ['domain', '域名信息'],
  ['text', '内容'],
  ['chart', '图表'],
  ['imgList', '图片'],
  ['table', '表格']
])
const downLoadData = () => {
  useExcel(response.table?.data, fileName.value || 'test')
}
</script>

<style scoped>

</style>
