<template>
  <div>

    <a-menu :dashed="true" v-model:selectedKeys="navCurrent" mode="horizontal">
      <a-menu-item v-for="(item) in nav" :key="item.path" :style="item.style">
        <template v-if="item.path==='doc'">
          <a href="//docs.spider-pro.cn" target="_blank">{{ item.text }}</a>
        </template>
        <template v-else>
          <router-link :class="item.class" :to="item.path">{{ item.text }}</router-link>
        </template>
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
              <a-avatar shape="square" style="background-color:#1890ff">
                <template #icon>
                  <UserOutlined/>
                </template>
              </a-avatar>
            </a>
            <template #overlay>
              <a-menu style="margin-top: 10px;">
                <a-menu-item>
                  <a-button type="text" @click="logout">
                    登出
                  </a-button>
                </a-menu-item>
                <a-menu-item>
                  <a-button type="text">
                    分享
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

<script setup lang="ts">
import nav from '@/data/nav'
import {
  UserOutlined,
  ShareAltOutlined,
  LogoutOutlined
} from '@ant-design/icons-vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { removeToken } from '@/utils/cookies'
import { account } from '@/apis/account/index'
import { toRefs, ref, onMounted } from 'vue'

const navCurrent = ref(['spider'])
const store = useStore()// account
const router = useRouter()

store.dispatch('userAsync')

// 当前导航位置

const { user } = toRefs(store.state.account)

const logout = () => {
  // 删除用户数据
  store.commit('deleteUser')
  // 删除用户任务
  store.commit('setTasks', [])
  //  清除本地cookie
  removeToken()
  // 跳转到登录页面
  router.push('account')
}
</script>

<style scoped>
/*.ant-menu-horizontal > .ant-menu-item-selected a{*/
/*  color: #87d068;*/
/*}*/
</style>
