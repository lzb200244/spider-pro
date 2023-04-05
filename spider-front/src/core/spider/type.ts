type domain = 'creation_date' | 'domain_name' | 'emails' | 'expiration_date' | 'name' | 'registrar'
export type DomainResponseAble = Record<domain, string>

// 表格的列
interface TableColumn {
  title: string;
  dataIndex: string;
  key: number;
  fixed?: 'left' | 'right' | null;
}

// 表格的数据
export interface Product {
  key: number;

  [key: string]: string | number;
}

// 爬虫响应
export interface SpiderResponseAble {
  domain: DomainResponseAble, // 域名消息
  imgList: Array<string> // 图片
  // echarts表格
  chart: {
    xData: Array<string> // x轴
    yData: Array<number>// y轴
  },
  table: {
    columns: Array<TableColumn>, // 表格的列
    data: Array<Product>, // 表格数据
  }
}

export type SpiderResponseOptionAble = Partial<SpiderResponseAble>

/**
 * 爬虫参数
 */
export interface SpiderConf {
  url: string; // 爬取的地址
  opt: string[]; // 爬取的选项
  type: string; // 爬取的类型（前后端分离？）
  mode: boolean; // 是否需要
  static: boolean; // 是否需要静态的
  email?: string; // 定时任务邮箱
  name?: string; // 定时任务名称
  time?: string; // 定时任务执行时间
  customOptions?: any[]; // 自定义选项
  [key: string]: any; // 其他可选参数
}
