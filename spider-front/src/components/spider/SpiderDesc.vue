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

<script lang="ts">
import ImgLoad from '@/components/layout/ImgLoad.vue'
import { computed } from 'vue'
import { domainResponseAble } from '@/module/views/spider'

export default {
  name: 'SpiderDesc',
  setup(props: { response: { imgList: string[]; domain: domainResponseAble } }) {
    const imgList = computed((): string[] => {
      /**
       * 图片
       */
      return props.response.imgList ? props.response.imgList : ['']
    })

    const domain = computed<domainResponseAble >(() => {
      /**
       * 域名消息
       *
       */
      // Object.keys().length===0
      return props.response?.domain ? props.response.domain : ({} as domainResponseAble)
    })

    return {
      imgList,
      domain
    }
  },
  props: {
    status: {
      type: Boolean,
      default: false
    },
    response: {
      type: Object
    }
  },
  components: {
    ImgLoad
  }

}
</script>

<style scoped>

</style>
