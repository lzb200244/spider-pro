import { createStore } from 'vuex'
import account from '@/store/modules/account/account'

export const store = createStore<State>({
  modules: {
    account

  }
})
