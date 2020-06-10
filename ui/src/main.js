import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { duration } from './filters'
import Tag from '@/components/Tag'
import Progress from '@/components/Progress'
import Voter from '@/components/Voter'
import User from '@/components/User'
import Fragment from 'vue-fragment'

Vue.use(Fragment.Plugin)

Vue.config.productionTip = false
Vue.component('Tag', Tag)
Vue.component('Progress', Progress)
Vue.component('Voter', Voter)
Vue.component('User', User)

Vue.filter('duration', duration)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
