/**
 # @Time : 2023/1/20 18:26
 # @Site : https://www.codeminer.cn
 """
 file-name:apis
 ex:
 """
 */

import { RawAxiosRequestConfig } from 'axios'

export const enum responseCode {
  /**
   * 响应code
   */
  Ok = 200,
  Created,
  Accepted,
  BadRequest = Ok + 200,
  Unauthorized,
  Forbidden = 403,
  RETRY_HTTP_CODES = 429, // 请求过多
  Error = Ok + 300
}

export interface ResponseAble {
  /**
   * 请求响应
   */
  code: number,
  msg: string | string[],
  data?: any,

}

export interface AccountFormAble {
  /**
   * 登录与注册接口
   */
  username: string,
  password: string,
  email?: string,
  rePassword?: string
}

export interface spiderDomainAble {
  /**
   * 爬虫配置
   */
  url: string,
  modules: string[],
  customOptions: any[]
}

export type AccountFormReadonly = Readonly<AccountFormAble>;
export type RequestConfig = RawAxiosRequestConfig
