import instance from '@/apis/index'
import { ResponseAble, spiderDomainAble } from '@/apis/type'
import { AccountFormReadonly } from '@/core/account/type'

/**
 * 注册
 * @param form
 */
const register = (form: AccountFormReadonly) => {
  return instance.post<ResponseAble>({
    url: 'account/register',
    data: { ...form }
  })
}
/**
 * 登录
 * @param form
 */
const login = (form: AccountFormReadonly) => {
  return instance.post<ResponseAble>({
    url: 'account/login',
    data: { ...form }
  })
}
/**
 * 获取用户信息
 */
const account = () => {
  return instance.get<ResponseAble>(
    { url: 'account/' }
  )
}

export {
  account, register, login
}
