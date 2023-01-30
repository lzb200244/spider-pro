import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

NProgress.configure({
  minimum: 0.08,
  showSpinner: true
  // parent: '#box1'
})

export function showFullLoading () {
  NProgress.start()
}

export function hideFullLoading () {
  NProgress.done()
}
