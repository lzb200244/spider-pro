/**
 * 校验
 */
const pattern = {
  password: /^(?=.*[A-Za-z])(?=.*\d)[^]{6,16}$/,
  username: /^[a-zA-Z0-9]{6,12}$/
}
type valid<T = never | string> = { (rule: any, value: string): Promise<T> }
const loginValidator: valid = (rule, value) => {
  // 输入是异步回到返回Promise对象
  return new Promise((resolve, reject) => {
    if (!pattern.username.test(value)) {
      reject(new Error('账号长度在6-16'))
    } else {
      resolve('success')
    }
  })
}
const passwordValidator: valid = (rule, value) => {
  // 输入是异步回到返回Promise对象
  return new Promise((resolve, reject) => {
    if (!pattern.password.test(value)) {
      reject(new Error('密码至少有1位字母且长度6-16'))
    } else {
      resolve('success')
    }
  })
}
const rulesMixin = {
  username: {
    type: 'string',
    asyncValidator: loginValidator
  },
  password: {
    type: 'string',
    asyncValidator: passwordValidator
  }
}
const Rules = {
  login: {
    ...rulesMixin
  },
  register: {
    ...rulesMixin,
    email: {
      type: 'email',
      message: '请输入正确的邮箱'
    }
  }

}

export default Rules
