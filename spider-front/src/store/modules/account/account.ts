// store.ts

import { MutationTree, ActionTree } from 'vuex'
import { account, getTasks } from '@/apis/account/index'
import { Tasks } from '@/apis/type'
import { State, Mutations, Actions, ITask } from '@/store/modules/account/type'
// 定义 state 的类型

// 初始化 state
const state: State = {
  user: '',
  tasks: {
    results: [],
    next: ''
  }
}

// 实现 mutations
const mutations: MutationTree<State> & Mutations = {
  setTasks(state, tasks) {
    state.tasks = tasks
  },
  setNextTask(state, next: string) {
    state.tasks.next = next
  },
  addTask(state, task) {
    // 底部
    state.tasks.results.unshift(...task)
  },
  deleteTask(state: State, id: string) {
    state.tasks.results = state.tasks.results.filter(item => item.task.id !== id)
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
    if (Object.values(state.tasks.results).length === 0) {
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
