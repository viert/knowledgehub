<template>
  <div class="question-list">
    <h3>Questions</h3>
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
      <QuestionsListItem v-for="question in questions" :key="question._id" :question="question" />
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import QuestionsListItem from './QuestionsListItem'

export default {
  data() {
    return {
      dataLoading: false
    }
  },
  components: {
    QuestionsListItem
  },
  computed: {
    ...mapState({
      questions: state => state.questions.questionsList
    }),
    currentSort() {
      return this.$route.query.sort ? this.$route.query.sort : 'rating'
    }
  },
  methods: {
    reload() {
      this.dataLoading = true
      const sort = this.currentSort
      this.$store.dispatch('questions/loadQuestions', { sort }).finally(() => {
        this.dataLoading = false
      })
    }
  },
  mounted() {
    this.reload()
  },
  watch: {
    '$route.query'() {
      this.reload()
    }
  }
}
</script>

<style lang="scss">
.question-list {
  padding: 8px;

  h3 {
    text-align: center;
    font-family: Montserrat;
    font-weight: 300;
    margin: 8px 0;
  }

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
</style>
