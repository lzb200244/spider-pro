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
  List,
  Statistic,
  Typography,
  DatePicker,
  TimePicker,
  Spin,
  Descriptions,
  Pagination,
  Image,
  Switch,
  Modal,
  Tag,
  AutoComplete,
  Select, Dropdown, Checkbox, Table, Popconfirm, Skeleton, Radio
} from 'ant-design-vue'

const ANTD = [
  Form,
  Radio,
  Tag,
  Skeleton,
  AutoComplete,
  Modal,
  Tabs,
  DatePicker,
  Popconfirm,
  Switch,
  Menu,
  Button,
  Typography,
  Input,
  Card,
  TimePicker,
  Statistic,
  List,
  Table,
  Empty,
  Spin, Descriptions, Select,
  Layout, Row, Col, Tooltip, Popover, Badge, Avatar, Pagination, Image, Dropdown, Checkbox

]

const app = createApp(App)
for (const antd of ANTD) {
  app.use(antd)
}

app.use(router)

app.use(store) // store对象
app.mount('#app')
