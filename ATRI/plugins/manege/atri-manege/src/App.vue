<template>
  <v-app>
    <v-navigation-drawer app v-model="drawer" class="na-d-0">
      <v-list
        nav
        dense
      >
        <v-list-item-group active-class="nattier-blue--text text--accent-4">
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-home</v-icon>
            </v-list-item-icon>
            <v-list-item-title>主页 | Home</v-list-item-title>
          </v-list-item>

          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-wrench</v-icon>
            </v-list-item-icon>
            <v-list-item-title>控制台 | Control</v-list-item-title>
          </v-list-item>

          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-database</v-icon>
            </v-list-item-icon>
            <v-list-item-title>数据 | Data</v-list-item-title>
          </v-list-item>

          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-comment-processing</v-icon>
            </v-list-item-icon>
            <v-list-item-title>聊天 | Chat</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="white" flat>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>ATRI Console</v-toolbar-title>
      
      <v-spacer></v-spacer>

      <v-btn href="https://jq.qq.com/?_wv=1027&k=iKLJzM1u" target="_blank" text>
        <span class="mr-2">Discuss</span>
        <v-icon small>mdi-qqchat</v-icon>
      </v-btn>

      <v-btn href="https://github.com/Kyomotoi/ATRI" target="_blank" text>
        <span class="mr-2">GitHub</span>
        <v-icon small>mdi-link-variant</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- 根据应用组件来调整你的内容 -->
    <v-main>

      <!-- 给应用提供合适的间距 -->
      <v-container fluid>

        <!-- 如果使用 vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app>
      <v-divider></v-divider>
      <v-container fluid>
        <v-row align="center" justify="center">
            <v-col class="text-center" cols="auto">
              <span> <v-icon>mdi-copyright</v-icon> Yours <strong>Kyomotoi</strong> </span>
            </v-col>
            <v-col class="text-center" cols="auto">
              <span> <v-icon>mdi-github</v-icon> <strong>ATRI</strong> </span>
            </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    drawer: true,
  }),
};
</script>

<style>
.text-center.a:visited {
  color: aliceblue;
}

.na-d-0 {
  background-image: url("https://i.loli.net/2021/07/19/WlFanrZHRQxb5Ay.png");
}
</style>