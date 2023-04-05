import * as XLSX from 'xlsx'
import { Product } from '@/core/spider/type'
import { message } from 'ant-design-vue'
export default function useExcel(products:Product[], title = 'test') {
  try {
    const data = XLSX.utils.json_to_sheet(products)// 此处tableData.value为表格的数据
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, data, 'sheet1')// test-data为自定义的sheet表名
    XLSX.writeFile(wb, `${title}.xlsx`)// test.xlsx为自定义的文件名
  } catch (e) {
    message.error('下载失败')
  }
}
