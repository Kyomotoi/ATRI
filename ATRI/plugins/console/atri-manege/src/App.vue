<template>
  <v-app>
    <v-navigation-drawer app v-model="drawer" class="na-d-0">
      <v-list
        nav
        dense
      >
        <v-list-item-group active-class="nattier-blue--text text--accent-4">
          <router-link to="/" tag="v-list-item-title">
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-home</v-icon>
              </v-list-item-icon>
              <v-list-item-title>主页 | Home</v-list-item-title>
            </v-list-item>
          </router-link>

          <router-link to="/control" tag="v-list-item-title">
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-wrench</v-icon>
              </v-list-item-icon>
              <v-list-item-title>控制面板 | Control</v-list-item-title>
            </v-list-item>
          </router-link>

          <router-link to="/data" tag="v-list-item-title">
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-database</v-icon>
              </v-list-item-icon>
              <v-list-item-title>数据 | Data</v-list-item-title>
            </v-list-item>
          </router-link>

          <router-link to="/chat" tag="v-list-item-title">
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-comment-processing</v-icon>
              </v-list-item-icon>
              <v-list-item-title>聊天 | Chat</v-list-item-title>
            </v-list-item>
          </router-link>

          <router-link to="/a-test" tag="v-list-item-title">
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-debug-step-over</v-icon>
              </v-list-item-icon>
              <v-list-item-title>测试 | Test</v-list-item-title>
            </v-list-item>
          </router-link>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="white" flat>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <router-link to="/" tag="v-toolbar-title">
        <v-toolbar-title>ATRI Console</v-toolbar-title>
      </router-link>
      
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

    <v-main>
      <v-container fluid>
        <v-lazy>
          <router-view></router-view>
        </v-lazy>
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
