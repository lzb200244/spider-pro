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
              <a-typography-title>介绍</a-typography-title>
              <a-typography-paragraph>
                蚂蚁的企业级产品是一个庞大且复杂的体系。这类产品不仅量级巨大且功能复杂，而且变动和并发频繁，常常需要设计与开发能够快速的做出响应。同时这类产品中有存在很多类似的页面以及组件，可以通过抽象得到一些稳定且高复用性的内容。
              </a-typography-paragraph>
              <a-typography-paragraph>
                随着商业化的趋势，越来越多的企业级产品对更好的用户体验有了进一步的要求。带着这样的一个终极目标，我们（蚂蚁金服体验技术部）经过大量的项目实践和总结，逐步打磨出一个服务于企业级产品的设计体系
                Ant Design。基于
                <a-typography-text mark>『确定』和『自然』</a-typography-text>
                的设计价值观，通过模块化的解决方案，降低冗余的生产成本，让设计者专注于
                <a-typography-text strong>更好的用户体验</a-typography-text>
                。
              </a-typography-paragraph>
              <a-typography-title :level="2">设计资源</a-typography-title>
              <a-typography-paragraph>
                我们提供完善的设计原则、最佳实践和设计资源文件（
                <a-typography-text code>Sketch</a-typography-text>
                和
                <a-typography-text code>Axure</a-typography-text>
                ），来帮助业务快速设计出高质量的产品原型。
              </a-typography-paragraph>
            </a-skeleton>
          </template>
          <template v-else-if="item==='imgList'">
            <template v-if="response.imgList?.length!==0">
              <img-load :imgList="response.imgList"/>
            </template>
          </template>
          <template v-else-if="item==='chart'">
            <charts :chart="response[item]"/>
          </template>
          <template v-else-if="item==='table' && response?.table">
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
import ImgLoad from '@/components/layout/ImgLoad.vue'
import Charts from '@/components/layout/Charts.vue'
import { SpiderResponseOptionAble } from '@/core/spider/type'
import { ref } from 'vue'
import useExcel from '@/hooks/useExcel'
interface Props {
  response: SpiderResponseOptionAble;

}

// eslint-disable-next-line vue/no-setup-props-destructure
const { response } = defineProps<Props>()
const visible = ref<boolean>(false)
const fileName = ref('test')
const loading = ref(true)

// 映射关系

const optMap = new Map<string, boolean>([
  ['domain', '域名信息'],
  ['content', '内容'],
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
