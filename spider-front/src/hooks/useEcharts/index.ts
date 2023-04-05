import * as echarts from 'echarts'
import type { Ref } from 'vue'
import { onMounted, ref, watch } from 'vue'
import { ChartData } from '@/hooks/useEcharts/types'

export default function useEcharts(
  domRef: Ref<HTMLDivElement>,
  data:ChartData
) {
  // Object.assign(data, )
  const baseConf = {
    title: {
      text: '某某数据',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    }
  }
  const option = {
    ...baseConf,
    xAxis: {
      type: 'category',
      data: data?.xData
    },
    yAxis: {
      type: 'value'
    },
    series: data?.yData?.map(item => {
      return {
        data: item,
        type: 'bar'
      }
    })

  }
  const chartOpt = {
    line: () => {
      Object.assign(option, {
        xAxis: {
          type: 'category',
          data: data?.xData
        },
        yAxis: {
          type: 'value'
        },
        series: data?.yData?.map(item => {
          return {
            data: item,
            type: 'line'
          }
        })
      })
    },
    bar: () => {
      Object.assign(option, {
        xAxis: {
          type: 'category',
          data: data?.xData
        },
        yAxis: {
          type: 'value'
        },
        series: data?.yData?.map(item => {
          return {
            data: item,
            type: 'bar'
          }
        })

      })
    },
    pie: () => {
      Object.assign(option, {
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: data?.yData[0]?.map((v, i) => {
              return {
                value: v,
                name: data?.xData[i]
              }
            }),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      })
    }
  }
  const initEcharts = () => {
    const myChart = echarts.init(domRef.value)
    data && myChart.setOption(option)
  }
  onMounted(() => {
    initEcharts()
  })
  return {
    initEcharts,
    chartOpt
  }
}
