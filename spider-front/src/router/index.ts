import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

// 2. 配置路由
const routes: Array<RouteRecordRaw> = [
  {
    path: '/account',
    component: () => import('@/views/Account.vue'),
    meta: {
      requireAuth: false,
      title: '登 录 | 注 册'
    }
  },
  {
    path: '/test',
    component: () => import('@/views/Test.vue'),
    meta: {
      requireAuth: false
    }
  },
  {
    path: '/tasks',
    component: () => import('@/views/Tasks.vue'),
    meta: {
      requireAuth: false,
      title: '定时任务'
    }
  },
  {
    path: '/spider',
    component: () => import('@/views/Spider.vue'),
    meta: {
      requireAuth: false,
      title: '爬 虫'
    }
  },
  {
    path: '',
    redirect: '/spider'
  }
]
// 1.返回一个 router 实列，为函数，里面有配置项（对象） history
const router = createRouter({
  history: createWebHistory(),
  routes
})
// 3导出路由   然后去 main.ts 注册 router.ts
export default router
