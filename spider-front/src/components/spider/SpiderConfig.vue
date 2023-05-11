<template>
  <div>
    <el-row>
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
            <a-radio-button value="example3">例子3</a-radio-button>
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
        <template v-if="type==='task'">
          <a-form-item
            label="任务名称"
            name="name"
            :rules="[{ required: true, message: '请输任务名称!' }]">
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
                       :rules="[{ required: true,message: '请选择执行时间' }, ]">
            <time-picker v-model="formConfig.time"/>
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
    </el-row>
    <el-row>
      <template v-if="type==='spider'">
        <Edit/>
      </template>
    </el-row>
  </div>

</template>

<script lang="ts" setup>
import Edit from '@/components/layout/Edit.vue'
import TimePicker from '@/components/layout/TimePicker.vue'
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue'
import { computed, defineEmits, reactive, ref, watch } from 'vue'
import { SpiderConf, Task } from '@/core/spider/type'
import { spiderDomain } from '@/apis/spider'
import { message } from 'ant-design-vue'
import { Timer } from '@/hooks/useTask/type'
import { store } from '@/store'

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
    case 'example3': {
      formConfig.opt = ['图片', '文本']
      formConfig.url = 'https://pixabay.com/'
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
  mode: false,
  static: false,
  type: props.type,

  // 无用的参数用来当零时的
  name: '',
  email: '',
  description: '',
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
const handleSearch = (val: string): void => {
  let res: { value: string }[]
  if (!val || val.indexOf('@') >= 0) {
    res = []
  } else {
    res = ['qq.com', '163.com', 'gmail.com'].map(domain => ({ value: `${val}@${domain}` }))
  }
  emailOption.value = res
}
const SendConfig = (form: SpiderConf) => {
  /**
   *  开始爬取
   */

  emits('startSpider')
  loading.value = true
  const status = true
  const task: Task = {} as Task
  if (formConfig.type === 'task') {
    Object.assign(
      task,
      {
        email: formConfig.email as string,
        name: formConfig.name as string,
        desc: formConfig.desc as string,
        rules: formConfig.time as Timer<any>
      })
    formConfig.task = task
  }
  Object.assign(
    formConfig, {
      email: undefined,
      name: undefined,
      description: undefined,
      time: undefined
    }
  )
  spiderDomain(formConfig).then(res => {
    // console.log(formConfig.time?.circle?.time)
    Object.assign(formConfig,
      {
        url: '',
        opt: [],
        mode: false,
        static: false,
        type: props.type,

        email: '',
        name: '',
        time: '',
        description: ''
      }
    )

    // 爬取成功
    emits('spiderSuccess', res.data, status)

    if (props.type === 'task') {
      store.commit('addTask', [res.data])
    }
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
