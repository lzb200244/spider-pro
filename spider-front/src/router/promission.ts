import router from '@/router/index'
import { message } from 'ant-design-vue'
import { RouteLocationNormalized, NavigationGuardNext } from 'vue-router'
import { showFullLoading, hideFullLoading } from '@/utils/process'
import { getToken } from '@/utils/cookies'

/**
 * 路由守卫
 */
router.beforeEach(
  (to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext) => {
    showFullLoading()

    const token = getToken() // get_token() ||
    if (typeof to.meta.title === 'string') {
      document.title = to.meta.title
    }
    if (token) {
      /**
       * 如果有token已经登录
       */
      to.meta.islogin = true
      if (to.path.includes('account')) {
        message.info('您已登入!!!')
        return next({ path: from.path ? from.path : '/' })
      }
    } else {
      // 需要登入的
      if (to.meta.requireAuth) {
        message.info('需要登入哦!')
        return next({ path: '/account', query: { next: to.path } })
      }
    }
    return next()
  })
router.afterEach(() => {
  hideFullLoading()
})

export default router
