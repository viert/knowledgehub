import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import QuestionsList from '@/views/Questions/QuestionsList.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/questions',
    name: 'QuestionsList',
    component: QuestionsList
  },
  {
    path: '/*',
    redirect: '/questions'
  }
]

const router = new VueRouter({
  routes
})

export default router
