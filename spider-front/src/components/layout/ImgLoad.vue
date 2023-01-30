<template>

  <div style="display: flex;justify-content: right">
    <a-checkbox v-model:checked="checkAll"
                :indeterminate="indeterminate"
                @change="onCheckAllChange">
      all
    </a-checkbox>
    <a-button @click="downloadImg">下载</a-button>
  </div>
  <div class="content m-md">
    <template v-for="(img) in Images" :key="img">
      <a-image
        width="60px"
        height="60px"
        :src="img"/>
      <a-checkbox :value="img" @change="select" ref="img" style="margin:  10px;"/>
    </template>
  </div>
  <div id="components-pagination-demo-mini" class="m-xl">
    <a-pagination size="small" v-model:current="currentPage" :total="checksList.length"/>
  </div>

</template>
<script lang="ts">
/**
 * 下载图片
 */
import download from 'downloadjs/download'
import { computed, onMounted, reactive, ref, toRefs, watch } from 'vue'
import { message } from 'ant-design-vue'
import { checkBoxAble, pagesConfAble, inputType } from '@/module/imgLoad'

export default {
  name: 'ImgLoad',
  setup(props: string[] | any) {
    const checkBox = reactive<checkBoxAble>({
      checksList: [],
      checkedList: [],
      checkAll: false
    })
    const pagesConf = reactive<pagesConfAble>({
      currentPage: 1,
      pageSize: 8
    })
    const indeterminate = ref(true)
    onMounted(() => {
      checkBox.checksList = props.imgList
    })
    const onCheckAllChange = () => {
      indeterminate.value = checkBox.checkAll
    }
    const select = (event: Event): void => {
      const dom = (event.target as inputType)
      dom.checked
        ? checkBox.checkedList.push((dom.value as string))
        : checkBox.checkedList = checkBox.checkedList.filter(_ => _ !== dom.value)
    }
    const downloadImg = (): void | never => {
      // 下载事件
      if (checkBox.checkedList.length !== 0) {
        checkBox.checkedList.forEach(item => {
          try {
            download(item)
          } catch (e) {
            message.info('图片下载失败')
            throw new Error('图片下载失败')
          }
        })
      }
    }
    const Images = computed(() => {
      return checkBox.checksList.slice((pagesConf.currentPage - 1) * 6, pagesConf.currentPage * 6)
    })

    // watch(checkedList, (newValue, oldValue) => {
    //   checkedList.value.length === checksList.value.length ? checkAll.value = true : ''
    // })
    return {
      indeterminate,
      Images,
      ...toRefs(checkBox),
      ...toRefs(pagesConf),
      downloadImg,
      select,
      onCheckAllChange
    }
  },

  props: {
    imgList: {
      type: Array

    }
  }

}

</script>
