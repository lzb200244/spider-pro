<template>

  <div>

    <a-button @click="downloadImg">下载</a-button>
  </div>
  <div class="content m-md">
    <template v-for="(img) in Images" :key="img">
      <a-image
        width="75px"
        height="75px"
        crossOrigin="anonymous"
        :src="img"/>
      <a-checkbox :value="img" @change="select" ref="img" style="margin: 10px;"/>
    </template>
  </div>
  <div class="m-xl" style="float: right">
    <a-pagination size="small" v-model:current="currentPage" :total="checksList.length"/>
  </div>

</template>
<script lang="ts">
/**
 * 下载图片
 */
import download from 'downloadjs/download'
import { computed, onMounted, reactive, ref, toRefs } from 'vue'
import { message } from 'ant-design-vue'

export default {
  name: 'ImgLoad',
  setup(props: string[] | any) {
    const checkBox = reactive<checkBoxAble>({
      checksList: [],
      checkedList: [],
      checkAll: false
    })
    // eslint-disable-next-line no-undef
    const pagesConf = reactive<pagesConfAble>({
      currentPage: 1,
      pageSize: 8
    })

    const indeterminate = ref(true)
    onMounted(() => {
      checkBox.checksList = props.imgList
    })
    const onCheckAllChange = () => {
      /**
       * 全选
       * */
      indeterminate.value = checkBox.checkAll
      // 权全选
      if (indeterminate.value) {
        checkBox.checkedList = checkBox.checksList
      } else {
        checkBox.checkedList = []
      }
    }
    const select = (event: Event): void => {
      /**
       * 选择下载图片
       */
      const dom = (event.target as inputType)
      dom.checked
        ? checkBox.checkedList.push((dom.value as string))
        : checkBox.checkedList = checkBox.checkedList.filter(_ => _ !== dom.value)
    }
    const downloadImg = (): void | never => {
      /**
       * 下载事件
       */

      if (checkBox.checkedList.length !== 0) {
        checkBox.checkedList.forEach(item => {
          // 放入promise里
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
      /**
       * 图片
       */
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
