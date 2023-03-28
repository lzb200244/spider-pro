// store.ts

import { MutationTree, ActionTree } from 'vuex'
import { account } from '@/apis/account/index'

// 定义 state 的类型

// 初始化 state
const state: State = {
  user: ''
}

// 实现 mutations
const mutations: MutationTree<State> & Mutations = {

  setUser(state, user: string) {
    state.user = user
  },

  deleteUser(state) {
    state.user = ''
  }
}

// 实现 actions
const actions: ActionTree<State, any> & Actions = {

  userAsync({ commit }) {
    account().then(res => {
      commit('setUser', res.data)
    })
  }
}

// 导出 store
export default {
  state,
  mutations,
  actions
}
