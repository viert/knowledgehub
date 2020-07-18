<script>
import { mapState } from 'vuex'
import { AuthStates } from '@/constants'

export default {
  data() {
    return {
      ready: false
    }
  },
  mounted() {
    this.checkAuthState()
    if (this.loggedIn) {
      // everything should be rendered on mounted already
      this.ready = true
    }
  },
  methods: {
    checkAuthState() {
      if (this.authState === AuthStates.LoggedOut) {
        this.$store.dispatch('users/setSigninOrigin', this.$route.fullPath)
        this.$router.replace('/signin')
        return false
      }
      return true
    }
  },
  computed: {
    ...mapState({
      authState: state => state.users.authState
    }),
    loggedIn() {
      return this.authState === AuthStates.LoggedIn
    }
  },
  watch: {
    authState() {
      this.checkAuthState()
    },
    loggedIn(nv) {
      // this is an ugly hack =(
      // when we come here while already logged in, the title input is already rendered
      // when logged out, it's not due to v-if="loggedIn".
      //
      // This means that if we're logged in and click the Ask Question button,
      // we can focus on title input right on mounted() callback
      // If we refresh this page, the title input is not rendered on mounted
      // before the authentication check cycle is complete. That's why we have a
      // 'ready' data field which is set to true in either case, i.e. when we're
      // sure the title input is rendered and can be focused on.
      // the next tick everything is going to be rendered
      if (nv) {
        this.$nextTick(() => {
          this.ready = true
        })
      }
    }
  }
}
</script>
