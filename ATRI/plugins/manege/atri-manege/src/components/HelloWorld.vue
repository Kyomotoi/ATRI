<template>
  <v-app>
    <!-- Running 将由 Fastpi控制
    正常：Running。非正常（刷新即丢失页面）Error。
    -->
    <h1 class="h1-index">ATRI is Running</h1>

    <v-divider></v-divider>
    
    <v-col>
      <h3 class="h3-index">主体状态 | Status</h3>
    </v-col>
    <v-container>
      <v-col>
        <v-row>
          <v-card height="170" width="400" class="ma-1">
            <!--同上：
            正常：Normal operation。断开：Waiting for connection-->
            <v-card-title>WS状态 | Websocket Status</v-card-title>
            <div class="text-center">
              <v-chip
                class="ma-2"
                color="green"
                text-color="white"
              >
                Normal operation
              </v-chip>
            </div>
          </v-card>

          <v-card height="170" width="400" class="ma-1">
            <v-card-title>自身状态 | Self Status</v-card-title>
            <div class="text-center">
              <v-chip
                class="ma-2"
                color="green"
                text-color="white"
              >
                Normal operation
              </v-chip>
            </div>
          </v-card>
        </v-row>
      </v-col>
    </v-container>

    <v-divider></v-divider>

    <v-col>
      <h3 class="h3-index">记录仪 | Dashboard</h3>
      <div id="container" class="test-box"></div>
    </v-col>
  </v-app>
</template>

<script>
import * as echarts from 'echarts'

export default {
  mounted() {
    let myChart = echarts.init(document.getElementById("container"));
    let option = {
      title: {
        subtext: '数据统计间隔：1分钟',
        left: '10'
      },
      legend: {
        data: ['接受信息', '发送信息', '服务调用速率', '服务调用失败速率']
      },
      color: ["#32c1e5", "#e5bb32", "#77e532", "#e5323e"],
       tooltip: {
        trigger: 'axis'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      axisPointer: {
        show: true,
      },
      dataZoom: [
        {
            type: 'slider',
            show: true,
            xAxisIndex: [0]
        },
        {
            type: 'slider',
            show: true,
            yAxisIndex: [0]
        },
        {
            type: 'inside',
            xAxisIndex: [0]
        },
        {
            type: 'inside',
            yAxisIndex: [0]
        }
      ],
      toolbox: {
        feature: {
          dataZoom: {
            yAxisIndex: false,
            xAxisIndex: false
          },
          restore: {},
          saveAsImage: {}
        }
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
          axisLine: {onZero: false},
          data: ["7-20 20:00", "7-20 20:01", "7-20 20:02", "7-20 20:03", "7-20 20:04", "7-20 20:05", "7-20 20:06", "7-20 20:07"]
        },
      ],
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '接受信息',
          type: 'line',
          data: [293, 394, 590, 493, 592, 489, 519, 528]
        },
        {
          name: '发送信息',
          type: 'line',
          data: [220, 182, 191, 234, 290, 330, 310, 230]
        },
        {
          name: '服务调用速率',
          type: 'line',
          data: [150, 232, 201, 154, 190, 330, 209, 291]
        },
        {
          name: '服务调用失败速率',
          type: 'line',
          data: [12, 3, 42 ,3, 32, 4, 42, 20]
        }
      ]
    };

    myChart.setOption(option);
    window.onresize = myChart.resize;
  }
}
</script>

<style>
.h1-index {
  font-size: 240%;
  color: #8f8f8f;
}

.h3-index {
  color: #8f8f8f;
}

.test-box {
  width: 100%;
  height: 600px;
  background-color: white;
}

</style>
