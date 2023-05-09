<template>
  <div ref="editContainer" class="code-editor"></div>
  <a-popover style="width: auto">
    <template #title>
      <a-button type="text" block>
        通过 xpath 解析
        <a href=""> 点击查看</a>
      </a-button>
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
    <a-button
      type="info"
      style="margin-top: 20px;"
      class=" float-right"
      @click="sendCustom"
    >
      提交
    </a-button>
  </a-popover>
</template>

<script>
import { getCurrentInstance, onMounted, watch, defineAsyncComponent, defineComponent } from 'vue'

// 动态导入 monaco-editor 代码

/**
 * 在线编辑器
 */

export default defineComponent({
  name: 'Edit',

  props: {
    value: {
      type: String,
      default: 'class CustomSpider(BaseSpider):\n        \n\tpass\n\tdef analysis(self,request):\n\t\t"""自定义规则"""\n\t\tpass\n\n'
    },

    language: {
      type: String,
      default: 'python'
    }
  },

  setup(props, { emit }) {
    let monacoEditor = null
    const DataItem = [{ title: "request.xpath('/html/p/text()')" }]

    const sendCustom = () => {
      console.log(monacoEditor.getValue())
    }

    const { proxy } = getCurrentInstance()

    const loadMonacoEditor = async () => {
      const monaco = await import('monaco-editor/esm/vs/editor/editor.main.js')
      self.MonacoEnvironment = {
        getWorker() {
          return new monaco.languages.typescript.TypeScriptWorker()
        }
      }
      return monaco
    }

    watch(
      () => props.value,
      (value) => {
        // 防止改变编辑器内容时光标重定向
        if (value !== monacoEditor?.getValue()) {
          monacoEditor.setValue(value)
        }
      }
    )

    onMounted(async () => {
      const monaco = await loadMonacoEditor()
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

    return { monacoEditor, sendCustom, DataItem }
  }
})
</script>

<style scoped>
.code-editor {
  width: 100%;
  min-height: 200px;
}
</style>
