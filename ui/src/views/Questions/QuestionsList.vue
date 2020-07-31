<template>
  <div class="page-layout">
    <main>
      <div class="question-list">
        <h3 class="page-title">Questions</h3>
        <ul class="question-sort-switch">
          <li
            class="question-sort-switch_item"
            :class="{
              'question-sort-switch_item--active': currentSort === 'rating'
            }"
          >
            <router-link to="/questions?sort=rating">Interesting</router-link>
          </li>
          <li
            class="question-sort-switch_item"
            :class="{
              'question-sort-switch_item--active': currentSort === 'date'
            }"
          >
            <router-link to="/questions?sort=date">Latest</router-link>
          </li>
        </ul>

        <div v-if="dataLoading" class="loading">
          <Progress text="loading" />
        </div>
        <ul v-else class="question-list_list">
          <QuestionsListItem
            v-for="question in questions"
            :key="question._id"
            :question="question"
          />
        </ul>
        <Pagination
          :current="currentPage"
          :total="totalPages"
          @page="pageChanged"
        />
      </div>
    </main>
    <aside>
      <EventsBlock />
    </aside>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { Question } from '@/store/types'
import QuestionsListItem from './QuestionsListItem.vue'
import EventsBlock from '@/views/Events/EventsBlock.vue'
import Pagination from '@/components/Pagination.vue'

const questions = namespace('questions')

@Component({
  components: {
    QuestionsListItem,
    Pagination,
    EventsBlock
  }
})
export default class QuestionsList extends Vue {
  private dataLoading = false

  @questions.State('questionsList') readonly questions!: Question[]
  @questions.State('page') readonly currentPage!: number
  @questions.State('totalPages') readonly totalPages!: number

  get currentSort() {
    return this.$route.query.sort ? this.$route.query.sort : 'rating'
  }

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

  pageChanged(page: number) {
    const { query } = this.$route
    this.$router.push({ query: { ...query, page: page.toString() } })
  }

  reload() {
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0
    this.dataLoading = true
    const sort = this.currentSort
    const page = this.page
    this.$store
      .dispatch('questions/loadQuestions', { sort, page })
      .catch(err => {
        if (err && err.maxPage) {
          this.pageChanged(err.maxPage)
        }
      })
      .finally(() => {
        this.dataLoading = false
      })
  }

  mounted() {
    this.reload()
  }

  @Watch('$route.query')
  onQueryChange() {
    this.reload()
  }
}
</script>

<style lang="scss">
.question-list {
  padding: 8px;

  .loading {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    height: calc(100vh - 280px);
  }
}

.question-sort-switch {
  display: flex;
  justify-content: flex-end;
  padding: 0;
  margin: 0 0 12px 0;
  list-style: none;
}

.question-sort-switch_item {
  margin-left: 8px;
  &--active {
    font-weight: bold;
    a {
      color: black;
    }
  }
}

.question-list_list {
  padding: 0;
  margin: 0;
  list-style: none;
}

h3.page-title {
  text-align: center;
  font-family: Montserrat;
  font-weight: 300;
  margin: 8px 0;
}
</style>
