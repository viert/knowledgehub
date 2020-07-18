import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Fragment from 'vue-fragment'
import Tag from '@/components/Tag.vue'
import Progress from '@/components/Progress.vue'
import Voter from '@/components/Voter.vue'

Vue.use(Fragment.Plugin)
Vue.config.productionTip = false
Vue.component('Tag', Tag)
Vue.component('Progress', Progress)
Vue.component('Voter', Voter)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
