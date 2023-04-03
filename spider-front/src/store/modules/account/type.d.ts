import { Tasks } from '@/apis/type'

interface State {
  // 用户信息
  user: string,
  tasks: any[]
}

interface Mutations {
  /**
   * 存储用户信息
   * @param state
   * @param user
   */
  setUser(state: State, user: string): void,

  deleteTask(state: State, id: string): void,

  setTasks(state: State, task: Array<Record<Tasks, string>>): void,

  addTask(state: State, tasks: Record<Tasks, string>): void,

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
  userAsync(context: any): void,

  /**
   * 获取用户任务列表
   * @param context
   */
  tasksAsync(context: any): void
}
