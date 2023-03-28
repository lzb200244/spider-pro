/**
 # @Time : 2023/1/20 18:26
 # @Site : https://www.codeminer.cn
 """
 file-name:apis
 ex:
 """
 */
import { RawAxiosRequestConfig } from 'axios'

/**
 * 响应code
 */
export const enum responseCode {

  Ok = 200,
  Created,
  Accepted,
  BadRequest = Ok + 200,
  Unauthorized,
  Forbidden = 403,
  RETRY_HTTP_CODES = 429, // 请求过多
  Error = Ok + 300
}

/**
 * 请求响应
 */
export interface ResponseAble {

  code: number,
  msg: string | string[],
  data?: any,

}

/**
 * 爬虫配置
 */
export interface spiderDomainAble {

  url: string,
  modules: string[],
  customOptions: any[]
}

export type RequestConfig = RawAxiosRequestConfig
