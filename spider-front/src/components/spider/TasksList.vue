<template>

  <a-list
    @scroll="handleScroll"
    style="overflow-y: auto;height: 500px"
    item-layout="vertical"
    :data-source="tasks.results"
    locale="暂时没有注册任务?"
    size="small"
    id="task"
  >
    <template #loadMore>
      <div style="text-align: center;margin: 30px auto">
        <a-spin v-show="isShow"/>
        <span id="noMore" style="color: #b4a7a7"></span>
      </div>

    </template>
    <template #renderItem="{ item }">
      <a-list-item>
        <template #actions>
          <a-popconfirm @confirm="deleteTask(item.task.id)" title="确认删除任务吗?" ok-text="Yes" cancel-text="No">
            <a href="#">删除</a>
          </a-popconfirm>

        </template>
        <a-skeleton :title="false" :loading="!!item.loading" active>
          <a-list-item-meta>
            <template #description>
              {{ item.task.description }}
              <el-row style="font-size: 10px">
                <a-col :span="24" style="float: right;">
                  <template v-if="item.task.start_time===null">
                    <a-tag color="processing">任务还未开始</a-tag>
                  </template>
                  <template v-else-if="parseInt(item.task.start_time)<Date.now()">
                    <a-tag color="success">任务已经完成</a-tag>
                  </template>
                  <template v-else>
                    <a-statistic-countdown title="执行时间" :value="parseInt(item.task.start_time)"
                                           format="D 天 H 时 m 分 s 秒"/>
                  </template>
                </a-col>
                <a-col :span="24">
                  <a-typography-link style="font-size: 18px" href="#">任务描述</a-typography-link>
                  <a-typography-paragraph class="m-sm">
                    {{ item.task.description || '没有描述' }}
                  </a-typography-paragraph>
                </a-col>
              </el-row>
            </template>
            <template #title>
              {{ item.task.name }}
            </template>
          </a-list-item-meta>
        </a-skeleton>
      </a-list-item>
    </template>
  </a-list>

</template>
<script lang="ts" setup>
import { useStore } from 'vuex'
import { computed, onMounted, ref } from 'vue'
import { delTask, getTasks } from '@/apis/account'
import { message } from 'ant-design-vue'

const store = useStore()
// 滑动请求加载
const isShow = ref(false)
onMounted(async () => {
  await store.dispatch('tasksAsync')
})

const tasks = computed(() => {
  return store.state.account.tasks
})
const handleScroll = async (event: Event) => {
  const el = event.target
  // todo bug 滑动太快查询重复请求相同页数，
  // 上加视口
  // el.scrollTop滚动上
  if (el.scrollTop + el.clientHeight >= el.scrollHeight) {
    // 判断是否正在加载数据，如果是则直接返回
    if (isShow.value) return

    isShow.value = true
    // 存在下一页
    const { next } = store.state.account.tasks
    if (next !== null) {
      // 判断下一页链接是否已经存在于 store 中，如果存在则直接返回
      const res = await getTasks(next)
      store.commit('setNextTask', res.data.next)
      store.commit('addTask', res.data.results)
    }
    if (next === null) {
      document.getElementById('noMore').innerText = '暂时没有更多数据了。。。'
    }

    isShow.value = false
  }
}

/**
 * 删除任务
 * @param id 任务标识
 */
const deleteTask = (id: string) => {
  delTask(id).then(res => {
    message.success('删除成功')
    store.commit('deleteTask', id)
  }).catch(res => {
    message.success(res.msg)
  })
}

</script>
<style scoped>
/* 隐藏默认滚动条 */

/* 自定义滚动条的样式 */
::-webkit-scrollbar {
  width: 6px; /* 滚动条宽度 */
  height: 6px; /* 滚动条高度 */
}

/* 滚动条背景 */
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* 滚动条上的滑块 */
::-webkit-scrollbar-thumb {
  background: #dcdcdc;
}

/* 鼠标悬停在滚动条上的滑块 */
::-webkit-scrollbar-thumb:hover {
  background: #c1c1c1;
}

</style>
