import Cookies from 'vue-cookie'

type Key = string

export function getToken(key: Key = 'JWT_TOKEN'): string {
  return Cookies.get(key)
}

// 设置token

export function setToken(key: Key, token: string):any {
  // 设置两个星期过期
  return Cookies.set(key, token, { expires: 60 * 24 * 24 * 14 })
}
/*
type setToken= { (key: Key, token: string): void }
export const setToken:setToken = function (key, token) {
  return Cookies.set(key, token, { expires: 60 * 24 * 24 * 14 })
}
 */

// 删除token
export function removeToken(key: Key = 'JWT_TOKEN') {
  return Cookies.delete(key)
}
