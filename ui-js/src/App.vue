<template>
  <div id="app">
    <MaintenancePage
      v-if="authState === AuthStates.Maintenance"
      @finished="getAuthStatus"
    />
    <Layout v-else />
    <AlertBox />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import Layout from '@/views/Layout'
import MaintenancePage from '@/views/MaintenancePage'
import AlertBox from '@/components/AlertBox'
import { AuthStates } from '@/constants'

export default {
  data() {
    return {
      AuthStates
    }
  },
  computed: {
    ...mapState({
      authState: state => state.users.authState
    })
  },
  components: {
    Layout,
    MaintenancePage,
    AlertBox
  },
  created() {
    this.$store.dispatch('data/loadAppInfo')
    this.$store.dispatch('users/loadAuthInfo')
  },
  methods: {
    ...mapActions({
      getAuthStatus: 'users/loadAuthInfo'
    })
  }
}
</script>

<style lang="scss">
@import './assets/common.scss';
</style>
