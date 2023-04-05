// store.ts

import { MutationTree, ActionTree } from 'vuex'
import { account, getTasks } from '@/apis/account/index'
import { Tasks } from '@/apis/type'
import { State, Mutations, Actions } from '@/store/modules/account/type'
// 定义 state 的类型

// 初始化 state
const state: State = {
  user: '',
  tasks: []
}

// 实现 mutations
const mutations: MutationTree<State> & Mutations = {
  setTasks(state: State, tasks: Array<Record<Tasks, string>>) {
    state.tasks = tasks
  },
  addTask(state: State, task: Record<Tasks, string>) {
    state.tasks.push(task)
  },
  deleteTask(state: State, id: string) {
    state.tasks = state.tasks.filter(item => item.id !== id)
  },
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
  },
  tasksAsync({ commit, state }) {
    if (state.tasks.length === 0) {
      getTasks().then(res => {
        commit('setTasks', res.data)
      })
    }
  }
}

// 导出 store
export default {
  state,
  mutations,
  actions
}
