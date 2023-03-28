<template>

  <a-table :columns="columns" :data-source="data">
    <template #headerCell="{ column }">
      <template v-if="column.key === 'name'">
        <span>
          <smile-outlined/>
          Name
        </span>
      </template>
    </template>

    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'name'">
        <a>
          {{ record.name }}
        </a>
      </template>
      <template v-else-if="column.key === 'tags'">
        <span>
          <a-tag
            v-for="tag in record.tags"
            :key="tag"
            :color="tag === 'loser' ? 'volcano' : tag.length > 5 ? 'geekblue' : 'green'"
          >
            {{ tag.toUpperCase() }}
          </a-tag>
        </span>
      </template>
      <template v-else-if="column.key === 'action'">
        <span>
          <a>Invite 一 {{ record.name }}</a>
          <a-divider type="vertical"/>
          <a>Delete</a>
          <a-divider type="vertical"/>
          <a class="ant-dropdown-link">
            More actions
            <down-outlined/>
          </a>
        </span>
      </template>
    </template>
  </a-table>

</template>
<script lang="ts">
import { useStore } from 'vuex'
import { SmileOutlined, DownOutlined } from '@ant-design/icons-vue'
import { defineComponent } from 'vue'

// import * as XLSX from 'xlsx'

const columns = [
  {
    name: 'Name',
    dataIndex: 'name',
    key: 'name'
  },
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age'
  },
  {
    title: 'Address',
    dataIndex: 'address',
    key: 'address'
  },
  {
    title: 'Tags',
    key: 'tags',
    dataIndex: 'tags'
  },
  {
    title: 'Action',
    key: 'action'
  }
]
const data = [
  {
    key: '1',
    name: 'John Brown',
    age: 32,
    address: 'New York No. 1 Lake Park',
    tags: ['nice', 'developer']
  },
  {
    key: '2',
    name: 'Jim Green',
    age: 42,
    address: 'London No. 1 Lake Park',
    tags: ['loser']
  },
  {
    key: '3',
    name: 'Joe Black',
    age: 32,
    address: 'Sidney No. 1 Lake Park',
    tags: ['cool', 'teacher']
  }
]
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles'
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles'
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles'
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles'
  }
]
export default defineComponent({
  components: {
    SmileOutlined,
    DownOutlined
  },
  setup() {
    const store = useStore()
    store.dispatch('userAsync')
    const a = 1
    return {
      data,
      columns,
      tableData
    }
  },
  mounted() {
    console.log('wlll')
    this.deriveExcel()
  },
  methods: {
    deriveExcel() {
      // const data = XLSX.utils.json_to_sheet(this.data)// 此处tableData.value为表格的数据
      //
      // const wb = XLSX.utils.book_new()
      // XLSX.utils.book_append_sheet(wb, data, 'test-data')// test-data为自定义的sheet表名
      // XLSX.writeFile(wb, 'test.xlsx')// test.xlsx为自定义的文件名
      // const workbook = XLSX.utils.table_to_book(document.querySelector('.ant-table-content table')) // 需要在table上定义一个id
      // try {
      //   XLSX.writeFile(workbook, 'BOX信息.xlsx')
      // } catch (e) {
      //
      // }
    }

  }

})
</script>
