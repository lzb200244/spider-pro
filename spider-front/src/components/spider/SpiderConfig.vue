<template>

  <a-form
    layout="vertical"
    :model="formConfig"
    name="basic"
    autocomplete="off"
    @finish="SendConfig">
    <a-form-item>
      <a-radio-group v-model:value="example">
        <a-radio-button value="example1">例子1</a-radio-button>
        <a-radio-button value="example2">例子2</a-radio-button>
      </a-radio-group>
    </a-form-item>
    <a-form-item
      label="URL"
      name="url"
      :rules="[{ required: true,type:'url', message: '请输正确网站地址!' }]">

      <a-input placeholder="请输入需要爬取的地址" v-model:value="formConfig.url"/>

    </a-form-item>
    <a-form-item
      label="选择模块"
      name="opt"
      :rules="[{ required: true, message: '请选择模块!' }]">
      <a-select
        v-model:value.trim="formConfig.opt"
        mode="multiple"
        style="width: 100%"
        :value="value"
        placeholder="请选择需要的模块(可多选)"
        :options="options"></a-select>
    </a-form-item>
    <template v-if="type==='spider'">
      <a-space
        v-for="(opt, index) in formConfig.customOptions"
        :key="opt.id"
        style="display: flex; margin-bottom: 8px"
        align="baseline">
        <a-form-item
          :label="`选择类型${index+1}`"
          :name="['customOptions', index, 'title']"
          :rules="{
          required: true,
          message: '选择类型',
          }">
          <a-input v-model:value="opt.title" placeholder="输入类型"/>
        </a-form-item>
        <a-form-item
          :label="`输入规则${index+1}`"
          :name="['customOptions', index, 'value']"
          :rules="{
          required: true,
          message: '输入规则',
       }">
          <a-input v-model:value="opt.value" placeholder="输入规则"/>
        </a-form-item>
        <MinusCircleOutlined @click="removeOption(opt)"/>
      </a-space>
      <a-form-item>
        <a-button type="dashed" block @click="addOption">
          <PlusOutlined/>
          增加规则
        </a-button>
      </a-form-item>
    </template>
    <template v-if="type==='task'">
      <a-form-item
        label="任务名称"
        name="name"
        :rules="[{ required: true, message: '请输任务名称!' }]"
      >
        <a-input v-model:value="formConfig.name" placeholder="任务名称"/>
      </a-form-item>
      <a-form-item
        label="发送的邮箱"
        name="email"
        :rules="[{ required: true,type:'email', message: '请输正确邮箱!' }]">
        <a-auto-complete
          v-model:value="formConfig.email"
          style="width: 200px"
          placeholder="请输入要发送的邮箱"
          :options="emailOption"
          @search="handleSearch"
        >
          <template #option="{ value: val }">
            {{ val.split('@')[0] }} @
            <span style="font-weight: bold">{{ val.split('@')[1] }}</span>
          </template>
        </a-auto-complete>
      </a-form-item>
      <a-form-item label="执行时间"
                   name="time"
                   :rules="[{ required: true,message: '选择日期' }, ]">
        <a-date-picker
          placeholder="选择执行时间"
          v-model:value="formConfig.time"
          value-format="YYYY-MM-DD HH:mm:ss"
          format="YYYY-MM-DD HH:mm:ss"
          :show-time="true"/>
      </a-form-item>
    </template>
    <a-form-item>
      <el-row>
        是否前后端分离
        <a-switch size="small" v-model:checked="formConfig.mode"/>
      </el-row>
      <el-row class="float-right">
        实时数据
        <a-switch size="small" v-model:checked="formConfig.static"/>
      </el-row>
    </a-form-item>
    <a-form-item>
      <a-button :loading="loading" :disabled="loading" type="primary" class="float-right" html-type="submit">
        确认
      </a-button>
    </a-form-item>
  </a-form>
  <template v-if="type==='spider'">
    <Edit/>
  </template>

</template>

<script lang="ts" setup>
import Edit from '@/components/layout/Edit.vue'
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue'
import { computed, defineEmits, reactive, ref, watch } from 'vue'
import { SpiderConf } from '@/core/spider/type'
import { spiderDomain } from '@/apis/spider'
import { message } from 'ant-design-vue'

const emailOption = ref<{ value: string }[]>([])
/**
 * 自动输入框
 */

const emits = defineEmits(['startSpider', 'spiderSuccess', 'spiderFailed'])

interface Props {
  mode: boolean,
  type: string
}

const props = withDefaults(defineProps<Props>(), {
  mode: true, type: 'spider'
})
const example = ref()
watch(example, value => {
  switch (value) {
    case 'example1': {
      formConfig.opt = ['图片']
      formConfig.url = 'https://unsplash.com/'
      break
    }
    case 'example2': {
      formConfig.opt = ['图片', '文本', '表格', '图表']
      formConfig.url = 'http://www.xinfadi.com.cn/index.html'
      break
    }
  }
})
/**
 * 配置项
 */
const formConfig = reactive<SpiderConf>({
  url: '',
  opt: [],
  customOptions: [],
  mode: false,
  static: false,
  type: props.type,
  email: '',
  name: '',
  time: ''
})
/**
 * 是否在加载状态
 * */
const loading = ref(false)
/**
 * 选项
 */
const options = computed(() => {
  const items = ['图片', '文本', '表格', '图表']
  return items.map(item => ({ value: item }))
})
/**
 * 添加选项
 */
const addOption = (): void => {
  formConfig.customOptions.push({
    title: '',
    value: '',
    id: Date.now()
  })
}
const handleSearch = (val: string): void => {
  let res: { value: string }[]
  if (!val || val.indexOf('@') >= 0) {
    res = []
  } else {
    res = ['gmail.com', '163.com', 'qq.com'].map(domain => ({ value: `${val}@${domain}` }))
  }
  emailOption.value = res
}

const removeOption = (item: any) => {
  /**
   * 移除选项
   */
  const index = formConfig.customOptions.indexOf(item)
  if (index !== -1) {
    formConfig.customOptions.splice(index, 1)
  }
}
const SendConfig = (form: SpiderConf) => {
  /**
   *  开始爬取
   */

  emits('startSpider')
  loading.value = true
  const status = true
  spiderDomain(formConfig).then(res => {
    Object.assign(formConfig,
      {
        url: '',
        opt: [],
        customOptions: [],
        mode: false,
        static: false,
        type: props.type,
        email: '',
        name: '',
        time: ''
      }
    )
    // 爬取成功
    emits('spiderSuccess', res.data, status)
    message.success(res.msg)
  }).catch(res => {
    emits('spiderFailed')
  }).finally(res => {
    loading.value = false
  })
}
</script>

<style scoped>

</style>
