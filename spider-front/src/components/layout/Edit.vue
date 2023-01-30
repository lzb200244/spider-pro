<template>

  <div ref="editContainer" class="code-editor">
  </div>
  <a-popover style="width: auto">
    <template #title>
      <a-button type="text" block>通过xpath解析 <a href=""> 点击查看</a></a-button>
    </template>
    <template #content>
      <a-list item-layout="horizontal" :data-source="DataItem">
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta>
              <template #title>
                <span>{{ item.title }}</span>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </template>
      </a-list>
    </template>
    <a-button type="info" style="margin-top: 20px;" class=" float-right" @click="sendCustom">提交</a-button>
  </a-popover>

</template>
<script>
import { getCurrentInstance, onMounted, watch, defineComponent } from 'vue'
import * as monaco from 'monaco-editor/esm/vs/editor/editor.main.js'
import JsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker'
/**
 * 在线编辑器
 */

// 解决vite Monaco提示错误

export default defineComponent({
  name: 'Edit',
  props: {
    value:
    // 可以传递code
        {
          type: String,
          default: `class CustomSpider(BaseSpider):
          \n\tpass\n\tdef analysis(self,request):\n\t\t"""自定义规则"""\n\t\tpass\n\n`
        },

    language: {
      type: String,
      default: 'python'
    }
  },

  setup(props, { emit }) {
    let monacoEditor = null
    const DataItem = [
      {
        title: "request.xpath('/html/p/text()')"
      }
    ]
    const sendCustom = () => {
      console.log(monacoEditor.getValue())
    }
    const { proxy } = getCurrentInstance()
    watch(
      () => props.value,
      (value) => {
        // 防止改变编辑器内容时光标重定向
        if (value !== monacoEditor?.getValue()) {
          monacoEditor.setValue(value)
        }
      }
    )

    onMounted(() => {
      self.MonacoEnvironment = {
        getWorker() {
          return new JsonWorker()
        }
      }
      monacoEditor = monaco.editor.create(proxy.$refs.editContainer, {
        value: props.value,
        readOnly: false,
        language: props.language,
        theme: 'vs-dark',
        acceptSuggestionOnEnter: 'smart', // 接受输入建议 "on" | "off" | ""
        selectOnLineNumbers: true,
        renderSideBySide: false
      })
      // 监听值变化

      monacoEditor.onDidChangeModelContent(() => {
        const currenValue = monacoEditor?.getValue()

        emit('update:value', currenValue)
      })
    })
    return {
      monacoEditor, sendCustom, DataItem
    }
  }

})
</script>
<style scoped>
.code-editor {
  width: 100%;
  min-height: 200px;
}
</style>
