<template>

  <a-list
    style="min-height: 300px"
    item-layout="vertical"
    :data-source="tasks.results"
    locale="暂时没有注册任务?"
    size="small"
  >
    <template #loadMore>
      <div
        v-if="tasks.results?.length!==0"
        :style="{ textAlign: 'center', marginTop: '12px', height: '32px', lineHeight: '32px' }">
        <a-button @click="onLoadMore">加载更多</a-button>
      </div>
    </template>
    <template #renderItem="{ item }">
      <a-list-item>
        <template #actions>
          <a-popconfirm @confirm="deleteTask(item.id)" title="确认删除任务吗?" ok-text="Yes" cancel-text="No">
            <a href="#">删除</a>
          </a-popconfirm>

          <a key="list-loadmore-more">more</a>
        </template>
        <a-skeleton :title="false" :loading="!!item.loading" active>
          <a-list-item-meta>
            <template #description>
              {{ item.desc }}
              <el-row style="font-size: 10px">
                <a-col :span="24" style="float: right;">
                  <template v-if="item.start_time===null">
                    <a-tag color="processing">任务还未开始</a-tag>
                  </template>
                  <template v-else-if="parseInt(item.start_time)*1000<Date.now()">
                    <a-tag color="success">任务已经完成</a-tag>
                  </template>
                  <template v-else>
                    <a-statistic-countdown title="执行时间" :value="parseInt(item.start_time)*1000"
                                           format="D 天 H 时 m 分 s 秒"/>
                  </template>
                </a-col>
                <a-col :span="24">
                  <a-typography-link style="font-size: 18px" href="#">任务描述</a-typography-link>
                  <a-typography-paragraph class="m-sm">
                    {{ item.desc || '没有描述' }}
                  </a-typography-paragraph>
                </a-col>
              </el-row>
            </template>

            <template #title>
              {{ item.name }}
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
import { delTask } from '@/apis/account'
import { message } from 'ant-design-vue'

const store = useStore()
onMounted(async () => {
  await store.dispatch('tasksAsync')
})

const tasks = computed(() => {
  return store.state.account.tasks
})
const onLoadMore = () => {
  console.log(tasks)
}
/**
 * 删除任务
 * @param id 任务标识
 */
const deleteTask = (id: string) => {
  store.commit('deleteTask', id)
  delTask(id).then(res => {
    message.success(res.msg)
  })
}

</script>
<style scoped>

</style>
