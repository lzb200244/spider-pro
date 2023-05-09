import Cookies from 'vue-cookie'

type Key = string

/**
 * 获取cookies
 * @param key
 */
export function getToken(key: Key = 'jwt-token'): string {
  return Cookies.get(key)
}

// 设置token
/**
 * 存储cookies过期时间
 * @param key
 * @param token cookie
 */
export function setToken(key: Key, token: string): any {
  return Cookies.set(key, token, { expires: 60 * 24 * 24 * 14 })
}

/*
type setToken= { (key: Key, token: string): void }
export const setToken:setToken = function (key, token) {
  return Cookies.set(key, token, { expires: 60 * 24 * 24 * 14 })
}
 */

/**
 * 删除token
 * @param key
 */
export function removeToken(key: Key = 'jwt-token') {
  // console.log(Cookies.delete(key))
  return Cookies.delete(key)
}
