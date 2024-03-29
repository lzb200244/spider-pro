/**
 # @Time : 2023/1/20 13:50
 # @Site : https://www.codeminer.cn
 """
 file-name:index
 ex:axios封装
 """
 */

// 引入 axios 实例
import { getToken } from '@/utils/cookies'
import { message } from 'ant-design-vue'
import axios, { AxiosRequestConfig, AxiosResponse, AxiosInstance } from 'axios'
import { RequestConfig, ResponseAble, responseCode } from './type'
import router from '@/router'

class Request<T> {
  private _instance: AxiosInstance // axios实例
  constructor(config: RequestConfig) {
    this._instance = axios.create(config)
    // 添加拦截器
    this._instance.interceptors.request.use(function (config: AxiosRequestConfig) {
      /**
       * 请求
       */
      // 在发送请求之前做些什么
      const token: string = getToken()
      console.log(token)
      //        'Content-Type': 'application/json',
      if (token) {
        console.log(config.headers)
        config.headers['jwt-token'] = token

        config.headers['Content-Type'] = 'application/json'
      }
      return config
    }, function (error) {
      // 对请求错误做些什么
      return Promise.reject(error)
    })
    this._instance.interceptors.response.use(function (response: AxiosResponse) {
      /**
       * 响应
       */
      // 2xx 范围内的状态码都会触发该函数。

      // 对响应数据做点什么
      // return response.data;
      const data: AxiosResponse = response.data

      return data
    }, function (error) {
      // 超出 2xx 范围的状态码都会触发该函数。
      const status: number = error.response.status

      const data:ResponseAble = error.response.data

      if (status >= responseCode.Error) {
        message.error('服务端错误error')
        return
      }
      switch (status) {
        case responseCode.Unauthorized: {
          if (data.code === 1203) {
            message.warning(data.msg)
          }
          // 未认证 （未登录
          return
        }
        case responseCode.Forbidden: {
          message.warning(data.msg)
          return router.push({
            path: 'account',
            query: {
              next: router.currentRoute.value.fullPath
            }
          })
        }
        case responseCode.RETRY_HTTP_CODES:
          message.warning('操作频率过快,已被限流,稍后在试试')
          window.location.href = 'https://www.baidu.com'
          return
      }

      if (data.msg) message.info(data.msg)
      // 对响应错误做点什么
      return Promise.reject(
        data
      )
    })
  }

  request<T>(config: RequestConfig): Promise<T> {
    return new Promise((resolve, reject) => {
      this._instance
        .request<any, any>(config)
        .then(res => {
          resolve(res)
        })
        .catch(err => {
          reject(err)
          return err
        })
    })
  }

  get<T>(config: RequestConfig): Promise<T> {
    return this.request<T>({
      ...config,
      method: 'get'
    })
  }

  post<T>(config: RequestConfig): Promise<T> {
    return this.request<T>({
      ...config,
      method: 'post'
    })
  }

  delete<T>(config: RequestConfig): Promise<T> {
    return this.request<T>({
      ...config,
      method: 'delete'
    })
  }

  patch<T>(config: RequestConfig): Promise<T> {
    return this.request<T>({
      ...config,
      method: 'patch'
    })
  }

  static getRules(): string {
    /**
     * 反代理
     */
    return Math.ceil(Math.random() * 5) + '' + new Date().getTime() + '' + Math.ceil(Math.random() * 5)
  }
}

const conf: RequestConfig = {
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 20000,
  headers: {
    'X-Custom-Header': `code-miner-${Request.getRules()}`
    // 反请求

  }
}
export default new Request(conf)
