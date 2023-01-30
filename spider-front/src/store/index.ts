import { InjectionKey } from 'vue'
import { createStore, Store } from 'vuex'

// 为 store state 声明类型
export interface State {
  user: string,

}

export const key: InjectionKey<Store<State>> = Symbol('account')
const state = {
  user: ''
}
export const store = createStore<State>({
  state,
  mutations: {
    saveUser (state, value) {
      // 保存用户信息
      state.user = value
    },
    deleteUser (state) {
      // 删除用户信息
      state.user = ''
    }
  }
})
