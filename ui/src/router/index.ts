import Vue from 'vue'
import VueRouter, { RouteConfig, NavigationGuardNext, Route } from 'vue-router'
import QuestionsList from '@/views/Questions/QuestionsList.vue'
import QuestionPage from '@/views/Questions/QuestionPage.vue'
import ProfileView from '@/views/Profile/ProfileView.vue'
import AskPage from '@/views/AskPage.vue'
import SigninPage from '@/views/SignIn/SigninPage.vue'
import SearchResultsPage from '@/views/Search/SearchResultsPage.vue'
import store from '@/store'

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
    path: '/search',
    name: 'SearchResults',
    component: SearchResultsPage
  },
  {
    path: '/questions/:questionId',
    name: 'QuestionPage',
    component: QuestionPage
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

router.beforeEach((to: Route, from: Route, next: NavigationGuardNext) => {
  if (to.name === 'SignIn') {
    const fullPath = from.fullPath ? from.fullPath : ''
    store.commit('users/setSigninOrigin', fullPath)
  }
  next()
})

export default router
