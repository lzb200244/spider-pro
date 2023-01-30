<template>
  <div>
    <a-menu :dashed="true" v-model:selectedKeys="navCurrent" mode="horizontal">
      <a-menu-item v-for="(item) in nav" :key="item.path" :style="item.style">
        <router-link :class="item.class" :to="item.path">{{ item.text }}</router-link>
      </a-menu-item>
      <a-menu-item :style="{marginLeft: 'auto',}" v-if="!user">
        <router-link to="account">
          <a-tooltip title="未登录" placement="top">
            <a-button>登录</a-button>
          </a-tooltip>
        </router-link>
      </a-menu-item>
      <a-menu-item :style="{marginLeft: 'auto'}" v-else>
        <router-link to="person">
          <a-dropdown>
            <a class="ant-dropdown-link" @click.prevent>
              <a-avatar style="background-color: #87d068">
                <template #icon>
                  <UserOutlined/>
                </template>
              </a-avatar>
            </a>
            <template #overlay>
              <a-menu style="margin-top: 20px;">
                <a-menu-item>
                  <a-button type="text" @click="logout">
                    登出
                    <template #icon>
                      <logout-outlined/>
                    </template>
                  </a-button>
                </a-menu-item>
                <a-menu-item>
                  <a-button type="text">
                    分享
                    <template #icon>
                      <share-alt-outlined/>
                    </template>
                  </a-button>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </router-link>
      </a-menu-item>
    </a-menu>
  </div>
</template>

<script>
import nav from '@/data/nav'
import {
  UserOutlined,
  ShareAltOutlined,
  LogoutOutlined
} from '@ant-design/icons-vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { removeToken } from '@/utils/cookies'
import { account } from '@/apis/request'
import { toRefs, ref, onMounted } from 'vue'
import { key } from '@/store'

export default {
  name: 'Header',
  components: {
    UserOutlined,
    ShareAltOutlined,
    LogoutOutlined
  },

  setup() {
    onMounted(() => {
      account().then(res => {
        // 保存用户对象
        // console.log(res.data)

        store.commit('saveUser', res.data)
      })
    })
    const store = useStore(key)// account
    const router = useRouter()
    const { user } = toRefs(store.state)
    const navCurrent = ref(['home'])

    const logout = () => {
      // 删除store信息
      store.commit('deleteUser')
      //  清除本地cookie
      removeToken()
      // 跳转到登录页面
      router.push('account')
    }
    return {
      nav,
      logout,
      user,
      navCurrent
    }
  }
}
</script>

<style scoped>

</style>
