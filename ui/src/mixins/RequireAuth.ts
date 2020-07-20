import { Vue, Component, Watch } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { AuthState } from '@/constants'

const users = namespace('users')

@Component
export default class RequireAuth extends Vue {
  @users.State('authState') authState!: AuthState

  get loggedIn() {
    return this.authState === AuthState.LoggedIn
  }

  onReady() {
    // To be overriden
  }

  mounted() {
    this.checkAuthState()
    if (this.loggedIn) {
      // everything should be rendered on mounted already
      this.onReady()
    }
  }

  checkAuthState() {
    if (this.authState === AuthState.LoggedOut) {
      this.$router.replace('/signin')
      return false
    }
    return true
  }

  @Watch('authState')
  onAuthStateChange() {
    this.checkAuthState()
  }

  @Watch('loggedIn')
  onLoggedInChange(newValue: boolean) {
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
    if (newValue) {
      this.$nextTick(() => {
        this.onReady()
      })
    }
  }
}
