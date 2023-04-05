import { createStore } from 'vuex'
import account from '@/store/modules/account/account'
import { State } from '@/store/modules/account/type'
export const store = createStore<State>({
  modules: {
    account

  }
})
