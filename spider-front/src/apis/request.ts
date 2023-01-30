import instance from './index'

import { AccountFormReadonly, ResponseAble, spiderDomainAble } from '@/module/apis'

const register = (form: AccountFormReadonly) => {
  return instance.post<ResponseAble>({
    url: 'account/register',
    data: { ...form }
  })
}
const login = (form: AccountFormReadonly) => {
  return instance.post<ResponseAble>({
    url: 'account/login',
    data: { ...form }
  })
}

const account = () => {
  return instance.get<ResponseAble>(
    { url: 'account/' }
  )
}

const spiderDomain = (from: spiderDomainAble) => {
  return instance.post<ResponseAble>({
    url: 'spider/domain',
    data: { ...from }
  })
}
export {
  account, spiderDomain, register, login
}
