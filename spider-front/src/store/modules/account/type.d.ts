interface State {
  // 用户信息
  user: string
}

interface Mutations {
  /**
   * 存储用户信息
   * @param state
   * @param user
   */
  setUser(state: State, user: string): void,
  /**
   * 删除用户信息
   */
  deleteUser(state: State): void
}

interface Actions {
  /**
   * 请求用户信息
   * @param context
   */
  userAsync(context: any): void
}
