import Vue from 'vue'
import VueRouter from 'vue-router'
import QuestionsList from '@/views/Questions/QuestionsList'
import QuestionView from '@/views/Questions/QuestionView'
import SigninPage from '@/views/SignIn/SigninPage'
import ProfileView from '@/views/Profile/ProfileView'
import AskPage from '@/views/AskPage'

Vue.use(VueRouter)

const routes = [
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
    path: '/ask',
    name: 'Ask',
    component: AskPage
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView
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
