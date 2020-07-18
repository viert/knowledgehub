import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import PageHeader from '@/views/PageHeader.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Page',
    component: PageHeader
  }
]

const router = new VueRouter({
  routes
})

export default router
