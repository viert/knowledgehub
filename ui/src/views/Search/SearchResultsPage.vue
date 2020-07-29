<template>
  <div class="page-layout search">
    <main>
      <div class="search-page">
        <Progress v-if="isLoading" text="Searching..." />
        <div v-else-if="q === ''" class="search-page_empty-query">
          Empty query
        </div>
        <div v-else class="search-results">
          <div v-if="searchResults.length === 0">
            Your query returned no results
          </div>
          <fragment v-else>
            <div class="search-results-count"></div>
            <ul class="search-results-list">
              <component
                v-for="item in searchResults"
                :key="item._id"
                :is="resultComponent(item)"
                :item="item"
                class="search-results-list_item"
              />
            </ul>
            <Pagination
              :current="currentPage"
              :total="totalPages"
              @page="pageChanged"
            />
          </fragment>
        </div>
      </div>
    </main>
    <aside>
      <div class="aside-section">
        <h4>Related Tags</h4>
        <div class="tag-list">
          <Tag v-for="tag in relatedTags" :key="tag" :name="tag" />
        </div>
      </div>
    </aside>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import Paginated from '@/mixins/Paginated'
import Pagination from '@/components/Pagination.vue'
import Progress from '@/components/Progress.vue'
import SearchResultsQuestion from './SearchResultsQuestion.vue'
import SearchResultsAnswer from './SearchResultsAnswer.vue'
import { namespace } from 'vuex-class'
import { Answer, Question } from '@/store/types'
import { mixins } from 'vue-class-component'

const questions = namespace('questions')

@Component({
  components: {
    Progress,
    Pagination,
    SearchResultsAnswer,
    SearchResultsQuestion
  }
})
export default class SearchResultsPage extends mixins(Paginated) {
  private isLoading = false

  @questions.State('searchResults') readonly searchResults!: Array<
    Answer | Question
  >
  @questions.State('count') readonly count!: number
  @questions.Getter('searchPageRelatedTags') readonly relatedTags!: string[]

  mounted() {
    this.$store.commit('questions/storeSearchResults', [])
    this.reload()
  }

  reload() {
    const payload = { query: this.q, page: this.page }
    this.isLoading = true
    this.$store
      .dispatch('questions/searchQuestions', payload)
      .catch(err => {
        if (err && err.maxPage) {
          this.pageChanged(err.maxPage)
        }
      })
      .finally(() => {
        this.isLoading = false
      })
  }

  resultComponent(item: Answer | Question) {
    if (item.type === 'answer') {
      return SearchResultsAnswer
    } else {
      return SearchResultsQuestion
    }
  }

  get q() {
    if (typeof this.$route.query.q === 'string') {
      return this.$route.query.q
    }
    return ''
  }
}
</script>

<style lang="scss">
.search-page {
  padding: 20px;
}

.page-layout.search .tag-list .tag {
  margin-bottom: 8px;
}

ul.search-results-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

li.answer,
li.question {
  border-top: 1px solid #dddddd;
  padding: 20px 0;
  &:first-child {
    border-top: none;
  }

  .answer-author,
  .question-author {
    font-size: 0.8em;
  }
}
</style>
