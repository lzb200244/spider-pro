import { computed, defineEmits, reactive, ref } from 'vue'
import { spiderDomainAble } from './type'
import { spiderDomain } from '@/apis/spider/index'
import { message } from 'ant-design-vue'
export default () => {
  const emit = defineEmits(['startSpider', 'spiderStatus'])
  /**
   * 配置项
   */
  const formConfig = reactive<spiderDomainAble>({
    url: 'https://unsplash.com/',
    modules: [],
    customOptions: []
  })
  /**
   * 是否在加载状态
   * */
  const loading = ref(false)
  /**
   * 选项
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
    emit('startSpider')
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
    formConfig, loading, options, addOption, SendConfig, removeOption
  }
}
