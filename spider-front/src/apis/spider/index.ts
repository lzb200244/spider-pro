import { ResponseAble, spiderDomainAble } from '@/apis/type'
import instance from '@/apis/index'

export const spiderDomain = (from: spiderDomainAble) => {
  return instance.post<ResponseAble>({
    url: 'spider/domain',
    data: { ...from }
  })
}
