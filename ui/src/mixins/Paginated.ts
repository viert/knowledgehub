import { Vue, Watch, Component } from 'vue-property-decorator'
import { namespace } from 'vuex-class'

const questions = namespace('questions')

@Component
export default class Paginated extends Vue {
  @questions.State('page') readonly currentPage!: number
  @questions.State('totalPages') readonly totalPages!: number

  get page() {
    let page = 1
    if (this.$route.query.page) {
      if (
        this.$route.query.page &&
        typeof this.$route.query.page === 'string'
      ) {
        page = parseInt(this.$route.query.page)
        if (isNaN(page)) {
          page = 1
        }
      }
    }
    return page
  }

  reload() {
    //
  }

  pageChanged(page: number) {
    const { query } = this.$route
    this.$router.push({ query: { ...query, page: page.toString() } })
  }

  @Watch('$route.query')
  onQueryChanged() {
    this.reload()
  }
}
