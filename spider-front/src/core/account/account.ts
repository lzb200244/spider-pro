/**
 # @Time : 2023/1/31 18:20
 # @Site : https://www.codeminer.cn
 """
 file-name:account
 ex:account.vue
 """
 */
import { useStore } from 'vuex'
import { message } from 'ant-design-vue'
import { register, login } from '@/apis/account/index'
import { setToken } from '@/utils/cookies'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { AccountFormReadonly } from './type'

export default () => {
  const router = useRouter()
  const store = useStore()
  const LoginFormState = reactive<Pick<AccountFormReadonly, 'password' | 'username'>>({
    username: '',
    password: ''
  })
  const RegisterFormState = reactive<AccountFormReadonly>({
    ...LoginFormState,
    email: '',
    rePassword: ''
  })
  const activeKey = ref<string>('login')
  /**
   * 确认密码校验
   */
  const rePasswordRules = {
    type: 'string',
    asyncValidator: (rule: string, value: string): Promise<string | null> => {
      // 确认密码校验
      return new Promise((resolve, reject) => {
        if (RegisterFormState.password !== value) {
          reject(new Error('两次密码不一致'))
        } else {
          resolve('success')
        }
      })
    }
  }

  /**
   * 登录
   * @param forms
   */
  const Login = (forms: AccountFormReadonly): void => {
    login(forms).then(res => {
      store.commit('setUser', res)
      // this.saveUser(res)
      setToken('JWT_TOKEN', res.data.token)
      message.success('登入成功')
      router.push('home')
    })
  }
  /**
   * 注册
   */
  const Register = (forms: AccountFormReadonly): void => {
    register(forms).then(res => {
      message.info('注册成功')
      activeKey.value = 'login'
    })
  }
  return {
    LoginFormState,
    RegisterFormState,
    activeKey,
    rePasswordRules,
    Register,
    Login

  }
}
