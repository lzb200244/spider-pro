<template>
  <a-card v-if="!status" title="爬取结果">
    <a-empty/>
  </a-card>
  <a-card v-else title="爬取结果" style="min-height: 300px">
    <template v-if="Object.keys(domain).length===0">
      <!--空对象-->
      <div style=" text-align: center;line-height: 300px">
        <a-spin tip="正在爬取. . ."/>
      </div>
    </template>
    <template v-else>
      <a-card title="域名信息" :bordered="false">
        <a-descriptions
          class="font-600"
          :column="{ xxl: 4, xl: 3, lg: 3, md: 3, sm: 2, xs: 1 }">

          <a-descriptions-item label="域名地址">{{ domain.domain_name }}</a-descriptions-item>
          <a-descriptions-item label="域名注册服务器">{{ domain.registrar }}</a-descriptions-item>
          <a-descriptions-item label="注册时间">{{ domain.creation_date }}</a-descriptions-item>
          <a-descriptions-item label="过期时间">{{ domain.expiration_date }}</a-descriptions-item>
          <a-descriptions-item label="注册邮箱">{{ domain.emails }}</a-descriptions-item>
          <a-descriptions-item label="户主">{{ domain.name }}</a-descriptions-item>
        </a-descriptions>
      </a-card>
      <a-card title="图片" :bordered="false">
        <img-load v-if="imgList.length!==0" :imgList="imgList"/>
      </a-card>
    </template>
  </a-card>
</template>

<script lang="ts" setup>

import ImgLoad from '@/components/layout/ImgLoad.vue'
import { computed } from 'vue'
import { spiderResponseAble, domainResponseAble } from '@/core/spider/type'
// eslint-disable-next-line vue/no-setup-props-destructure
const { response } = defineProps<{
  response: spiderResponseAble;

}>()

const imgList = computed((): string[] => {
  return response.imgList ? response.imgList : ['']
})

const domain = computed<domainResponseAble>({
  get: () => {
    /**
     * 域名消息
     *
     */

    return response?.domain ? response.domain : ({} as domainResponseAble)
  }
})

</script>

<style scoped>

</style>
