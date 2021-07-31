import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: '主页 | Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/control',
    name: '控制面板 | Control',
    component: () => import('../views/Control.vue')
  },
  {
    path: '/data',
    name: '数据 | Data',
    component: () => import('../views/Data.vue')
  },
  {
    path: '/chat',
    name: '聊天 | Chat',
    component: () => import('../views/Chat.vue')
  },
  {
    path: '/a-test',
    name: '测试 | Test',
    component: () => import('../views/Test.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
