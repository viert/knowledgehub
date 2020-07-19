<template>
  <div id="app">
    <MaintenancePage v-if="maintenance" @finished="getAuthStatus" />
    <Layout v-else />
    <AlertBox />
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { AuthState } from './constants'
import { namespace } from 'vuex-class'
import AlertBox from '@/components/AlertBox.vue'
import MaintenancePage from '@/views/MaintenancePage.vue'
import Layout from '@/views/Layout.vue'
const users = namespace('users')

@Component({
  components: {
    MaintenancePage,
    AlertBox,
    Layout
  }
})
export default class App extends Vue {
  @users.State('authState') authState!: AuthState
  @users.Action('loadAuthInfo') loadAuthInfo!: () => void

  get maintenance() {
    return this.authState === AuthState.Maintenance
  }

  created() {
    this.$store.dispatch('data/loadAppInfo')
    this.$store.dispatch('users/loadAuthInfo')
  }
}
</script>

<style lang="scss">
@import './assets/common.scss';
</style>
