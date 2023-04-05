import { ResponseAble } from '@/apis/type'

import instance from '@/apis/index'
import { SpiderConf } from '@/core/spider/type'
export const spiderDomain = (from: SpiderConf) => {
  return instance.post<ResponseAble>({
    url: 'spider/domain',
    data: { ...from }
  })
}
