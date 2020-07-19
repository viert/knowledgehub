import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import QuestionsList from '@/views/Questions/QuestionsList.vue'
import AskPage from '@/views/AskPage.vue'
import SigninPage from '@/views/SignIn/SigninPage.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/questions',
    name: 'QuestionsList',
    component: QuestionsList
  },
  {
    path: '/signin',
    name: 'SignIn',
    component: SigninPage
  },
  {
    path: '/questions/:questionId',
    name: 'QuestionView',
    component: QuestionView
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView
  },
  {
    path: '/ask',
    name: 'AskPage',
    component: AskPage
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
