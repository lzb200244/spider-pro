<template>
  <a-card title="输入配置项">
    <template #extra><a href="#">more</a></template>
    <a-form
      :model="formConfig"
      name="basic"
      autocomplete="off"
      @finish="SendConfig">
      <a-form-item
        label="URL"
        name="url"
        :rules="[{ required: true,type:'url', message: '请输正确网站地址!' }]">
        <a-input v-model:value="formConfig.url"/>
      </a-form-item>
      <a-form-item
        label="选择模块"
        name="modules"
        :rules="[{ required: true, message: '请选择模块!' }]">
        <a-select
          v-model:value.trim="formConfig.modules"
          mode="multiple"
          style="width: 100%"
          placeholder="请选择需要的模块(可多选)"
          :options="options"></a-select>
      </a-form-item>
      <a-space
        v-for="(modules, index) in formConfig.customOptions"
        :key="modules.id"
        style="display: flex; margin-bottom: 8px"
        align="baseline">
        <a-form-item
          :label="`选择类型${index+1}`"
          :name="['customOptions', index, 'title']"
          :rules="{
          required: true,
          message: '选择类型',}">
          <a-input v-model:value="modules.title" placeholder="输入类型"/>
        </a-form-item>
        <a-form-item
          :label="`输入规则${index+1}`"
          :name="['customOptions', index, 'value']"
          :rules="{
          required: true,
          message: '输入规则',
       }">
          <a-input v-model:value="modules.value" placeholder="输入规则"/>
        </a-form-item>
        <MinusCircleOutlined @click="removeOption(modules)"/>
      </a-space>
      <a-form-item>
        <a-button type="dashed" block @click="addOption">
          <PlusOutlined/>
          增加规则
        </a-button>
      </a-form-item>
      <a-form-item>
        <a-button :loading="loading" :disabled="loading" type="primary" class="float-right" html-type="submit">
          Spider
        </a-button>
      </a-form-item>
    </a-form>
    <Edit/>
  </a-card>
</template>

<script lang="ts" setup>
import Edit from '@/components/layout/Edit.vue'
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue'
import useConf from '@/core/spider/spiderConf'
const {
  formConfig, loading, options, addOption, removeOption, SendConfig
} =
useConf()

</script>

<style scoped>

</style>
