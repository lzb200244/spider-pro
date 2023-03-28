/**
 * 登录与注册接口
 */
export interface AccountFormAble {
  username: string, // 账号
  password: string, // 密码
  email: string, // 邮箱
  rePassword: string // 确认密码
}
export type AccountFormReadonly = Readonly<AccountFormAble>;
