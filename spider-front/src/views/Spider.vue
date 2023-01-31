<template>
  <a-layout-content class="">
    <a-row>
      <a-col :md="24" :xs="24" :lg="12" class="p-sm">
        <a-card title="输入配置项">
          <spider-config @spiderStatus='spiderStatus' @spider='spider'/>
        </a-card>
      </a-col>
      <a-col :md="24" :xs="24" :lg="12" class="p-sm">
        <spider-desc :response="response" :status="status"/>
      </a-col>
    </a-row>
  </a-layout-content>
</template>

<script lang="ts">

import SpiderConfig from '@/components/spider/SpiderConfig.vue'
import SpiderDesc from '@/components/spider/SpiderDesc.vue'
import { ref } from 'vue'

export default {
  components: {
    SpiderConfig,
    SpiderDesc
  },
  name: 'Home',
  setup() {
    const status = ref<boolean>(false)
    const response = ref<spiderResponseOptionAble>()
    const spider = (): void => {
      status.value = true
    }
    const spiderStatus = (data: spiderResponseOptionAble, status = true): void => {
      response.value = data
    }
    return {
      status,
      response,
      spider,
      spiderStatus
    }
  }

}
</script>

<style scoped>

</style>
