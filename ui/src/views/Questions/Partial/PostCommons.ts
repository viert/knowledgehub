import { Vue, Component } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { User } from '@/store/types'

const users = namespace('users')
const questions = namespace('questions')

@Component
export default class PostCommons extends Vue {
  @users.Getter('user') getUser!: (id: string) => User
  @questions.Getter('isMyQuestion') readonly isMyQuestion!: boolean

  scrollIntoView() {
    const rootElement = this.$refs.root as HTMLElement
    rootElement.scrollIntoView({ block: 'center' })
  }
}
