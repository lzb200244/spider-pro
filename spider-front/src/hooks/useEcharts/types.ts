export type chart = 'bar' | 'line' | 'pie'

export interface ChartData {
  // x轴列名
  xData: Array<string>,
  // y轴相当于数据值
  yData: Array<Array<number>>
}
