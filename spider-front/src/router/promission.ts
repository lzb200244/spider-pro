import router from '@/router/index'
import { message } from 'ant-design-vue'
import { RouteLocationNormalized, NavigationGuardNext } from 'vue-router'
import { showFullLoading, hideFullLoading } from '@/utils/process'

/**
 * 路由守卫
 */
router.beforeEach(
  (to:RouteLocationNormalized,
    from:RouteLocationNormalized,
    next:NavigationGuardNext) => {
    showFullLoading()
    const token = false // get_token() ||
    if (token) {
      /**
       * 如果有token已经登录
       */
      to.meta.islogin = true
      if (to.path === '/account') {
        message.info('您已登入!!!')
        return next({ path: from.path ? from.path : '/' })
      }
    } else {
    // 需要登入的
      if (to.meta.requireAuth) {
        message.info('需要登入哦!')
        return next({ path: '/account' })
      }
    }
    return next()
  })
router.afterEach(() => {
  hideFullLoading()
})

export default router
