import { createApp } from 'vue'
import App from './App.vue'
import 'ant-design-vue/dist/antd.css'
import router from '@/router/promission'
import 'ant-design-vue/lib/date-picker/style/css'
import { store } from '@/store'
import '../index.css'
import {
  Form,
  Tabs,
  Button,
  Input,
  Layout,
  Menu,
  Row,
  Col,
  Tooltip,
  Popover,
  Badge,
  Avatar,
  Card,
  Empty,
  Spin,
  Descriptions,
  Pagination,
  Image,
  Select, Dropdown, Checkbox, Table
} from 'ant-design-vue'

const ANTDS = [
  Form,
  Tabs,
  Menu,
  Button,
  Input,
  Card,
  Table,
  Empty,
  Spin, Descriptions, Select,
  Layout, Row, Col, Tooltip, Popover, Badge, Avatar, Pagination, Image, Dropdown, Checkbox

]

const app = createApp(App)
ANTDS.forEach(item => {
  app.use(item)
})
app.use(router)

app.use(store) // store对象
app.mount('#app')
