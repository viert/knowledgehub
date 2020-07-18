import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Fragment from 'vue-fragment'
import Tag from '@/components/Tag.vue'

Vue.use(Fragment.Plugin)
Vue.config.productionTip = false
Vue.component('Tag', Tag)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
