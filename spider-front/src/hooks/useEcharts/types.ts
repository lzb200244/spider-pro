
export type chart = 'bar'|'line' |'pie'
export interface ChartData {
  xData:Array<string>,
  yData:Array<Array<number>>
}
