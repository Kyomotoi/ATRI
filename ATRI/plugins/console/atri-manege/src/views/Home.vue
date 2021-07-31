<template>
  <v-app>
    <h1 class="h1-index">ATRI is Running</h1>

    <v-divider></v-divider>
    
    <v-col>
      <h3 class="h3-index">主体状态 | Status</h3>
    </v-col>
    <v-container>
      <v-col>
        <v-row>
          <v-card height="170" width="400" class="ma-1">
            <v-card-title>WS状态 | Websocket Status</v-card-title>
            <div class="text-center">
              <v-chip
                class="ma-2"
                color="green"
                text-color="white"
              >
                <div id="isConnect"></div>
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
                <div id="selfStatus"></div>
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
    function sleep (time) {
      return new Promise((resolve) => setTimeout(resolve, time));
    }

    function isConnect() {
      try {
        var url = "http://127.0.0.1:20000/bot/is_connect"
        var req = new XMLHttpRequest();
        req.open("get", url);
        req.send(null);
        req.onload = function() {
          if (req.status == 200) {
            let data = JSON.parse(req.responseText);
            if (data.is_connect) {
              document.getElementById("isConnect").innerHTML = "Connected";
            } else {
              document.getElementById("isConnect").innerHTML = "Lost Connection";
            }
          } else {
            document.getElementById("isConnect").innerHTML = "Failed to get DATA";
          }
        }
      } catch {
        document.getElementById("isConnect").innerHTML = "ERROR";
      }
    }

    function getStatus() {
      try {
        var url = "http://127.0.0.1:20000/bot/status"
        var req = new XMLHttpRequest();
        req.open("get", url);
        req.send(null);
        req.onload = function() {
          if (req.status == 200) {
            let data = JSON.parse(req.responseText);
            document.getElementById("selfStatus").innerHTML = data.message;
          }
        }
      } catch {
        document.getElementById("isConnect").innerHTML = "ERROR";
      }
    }

    function dashboard() {
      var data_time = ["0"];
      var data_msg = [0];
      var data_health = [0];
      var data_error = [0];

      try {
        var url = "http://127.0.0.1:20000/bot/dashboard_info"
        var req = new XMLHttpRequest();
        req.open('GET', url);
        req.send(null);
        req.onload = function () {
          var t_data = JSON.parse(req.responseText);
          var t_data_l = t_data.data
          for (var i = 0; i < t_data_l.length; i++) {
            data_time.push(t_data_l[i].time)
            data_msg.push(t_data_l[i].freq_data.msg)
            data_health.push(t_data_l[i].freq_data.health)
            data_error.push(t_data_l[i].freq_data.error)
          }
        }
      } catch {
        document.getElementById("container").innerHTML = "Failed to get DATA!"
        return
      }

      sleep(100).then(
        () => {
          let myChart = echarts.init(document.getElementById("container"));
          let option = {
            title: {
              subtext: '数据统计间隔：1分钟',
              left: '10'
            },
            legend: {
              data: ['接受信息', '服务调用成功速率', '服务调用失败速率']
            },
            color: ["#2d85f0", "#ffbc32", "#f4433c"],
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
                  xAxisIndex: [0],
                  start: 70,
                  end: 100
              },
              {
                  type: 'slider',
                  show: true,
                  yAxisIndex: [0]
              },
              {
                  type: 'inside',
                  xAxisIndex: [0],
                  start: 70,
                  end: 100
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
                data: data_time
              },
            ],
            yAxis: {
              type: 'value'
            },
            series: [
              {
                name: '接受信息',
                type: 'line',
                areaStyle: {},
                data: data_msg
              },
              {
                name: '服务调用成功速率',
                type: 'line',
                areaStyle: {},
                data: data_health
              },
              {
                name: '服务调用失败速率',
                type: 'line',
                areaStyle: {},
                data: data_error
              }
            ]
          };

          console.info(data_time);
          console.info(data_msg);
          console.info(data_error);
          myChart.setOption(option);
          window.onresize = myChart.resize;
        }
      )
    }

    setInterval(isConnect(), 100);
    setInterval(getStatus(), 1000);
    setInterval(dashboard(), 6000);
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
  height: 500px;
  background-color: white;
}

</style>
