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

import { key } from '@/store'
import { register, login } from '@/apis/request'
import { setToken } from '@/utils/cookies'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { AccountFormReadonly } from '@/module/apis'
// import cav from '@/assets/js/canvas'

export default () => {
  const router = useRouter()
  const store = useStore(key)
  const LoginFormState = reactive<AccountFormReadonly>({
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
   */
  const Login = (forms: AccountFormReadonly): void => {
    /*
      关闭滑动校验功能
      if (!this.$refs.child.isSuccess()) {
      return message.info('请完成验证!')
    }
     */
    login(forms).then(res => {
      store.commit('saveUser', res)
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
