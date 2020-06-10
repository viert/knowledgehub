import Vue from 'vue'
import VueRouter from 'vue-router'
import QuestionsList from '@/views/Questions/QuestionsList'
import QuestionView from '@/views/Questions/QuestionView'

Vue.use(VueRouter)

const routes = [
  {
    path: '/questions',
    name: 'QuestionsList',
    component: QuestionsList
  },
  {
    path: '/questions/:questionId',
    name: 'QuestionView',
    component: QuestionView
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
