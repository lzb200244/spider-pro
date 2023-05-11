<template>
    <a-row>
      <a-col :md="24" :xs="24" :lg="12" class="p-sm">
        <a-card title="输入配置项">
          <spider-config :type="'task'" />
        </a-card>
      </a-col>
      <a-col :md="24" :xs="24" :lg="12" class="p-sm">
        <a-card title="任务列表">
          <tasks-list v-model:value="value"/>
        </a-card>
      </a-col>
    </a-row>

</template>

<script setup lang="ts">
import SpiderConfig from '@/components/spider/SpiderConfig.vue'
import TasksList from '@/components/spider/TasksList.vue'

</script>

<style scoped>

</style>
