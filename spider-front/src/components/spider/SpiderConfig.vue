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

<script lang="ts">
import { message } from 'ant-design-vue'
import { spiderDomain } from '@/apis/request'

import Edit from '@/components/layout/Edit.vue'
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue'
import { computed, reactive, ref } from 'vue'
import { spiderDomainAble } from '@/module/apis'

export default {
  name: 'SpiderConfig',
  emits: ['spider', 'spiderStatus'],
  setup(props :any, { emit }:any) {
    /**
     * 配置项
     */
    const formConfig = reactive<spiderDomainAble>({
      url: 'https://unsplash.com/',
      modules: [],
      customOptions: []
    })
    const loading = ref<boolean>(false)
    /**
     * 选项计算
     */
    const options = computed(() => {
      const items = ['图片', '文章', '表格']
      return items.map(item => ({ value: item }))
    })
    /**
     * 添加选项
     */
    const addOption = ():void => {
      formConfig.customOptions.push({
        title: '',
        value: '',
        id: Date.now()
      })
    }
    const SendConfig = (form:spiderDomainAble) => {
      /**
       *  开始爬取
       */
      emit('spider')
      loading.value = true
      Object.assign(form, { modules: Object.keys(form.modules) })
      spiderDomain(form).then(res => {
        loading.value = false
        emit('spiderStatus', res.data, true)
        message.success(res.msg)
      })
    }
    const removeOption = (item:any) => {
      /**
       * 溢出选项
       */
      const index = formConfig.customOptions.indexOf(item)
      if (index !== -1) {
        formConfig.customOptions.splice(index, 1)
      }
    }
    return {
      loading,
      formConfig,
      options,
      addOption,
      SendConfig,
      removeOption
    }
  },
  components: {
    PlusOutlined,
    MinusCircleOutlined,
    Edit
  }

}
</script>

<style scoped>

</style>
