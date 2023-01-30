<template>
  <a-row justify="center ">
    <a-col class="mx">
      <a-tooltip placement="topLeft">
        <template #title>
          <span>项目开源</span>
        </template>
        <github-outlined/>

        <a href="https://gitee.com/codesMines/spider-pro"> 开源支持</a>
      </a-tooltip>

    </a-col>
    <a-col class="mx">
      <a-popover title="Author : QQ">
        <template #content>
          <a-badge :count="1">
            <a-avatar shape="square">
              <template #icon>
                <UserOutlined/>
              </template>
            </a-avatar>

          </a-badge>
          <span style="margin-left: 10px;">2632141215</span>
        </template>
        <qq-outlined/>
        作者QQ
      </a-popover>
    </a-col>
    <a-col class="mx">
      <a-tooltip placement="topLeft">
        <template #title>
          <span>反馈</span>
        </template>
        <bug-outlined/>
        <a href="https://support.qq.com/product/487770"> 反 馈</a>
      </a-tooltip>

    </a-col>
    <a-col class="mx">
      <a-tooltip placement="topLeft">
        <template #title>
          <span>分享</span>
        </template>
        <share-alt-outlined/>
        分享
      </a-tooltip>

    </a-col>
  </a-row>
</template>

<script>
import {
  GithubOutlined, QqOutlined,
  BugOutlined, UserOutlined, ShareAltOutlined
} from '@ant-design/icons-vue'

export default {
  name: 'Footer',
  components: {
    GithubOutlined,
    QqOutlined,
    ShareAltOutlined,
    BugOutlined,
    UserOutlined
  },
  setup() {
    return {}
  }
}
</script>

<style scoped>
.mx {
  margin: 0 30px;
}

a {
  color: #666;
}

a:hover {
  color: #41B883;
}
</style>
