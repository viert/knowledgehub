<template>
  <div class="page-layout">
    <main>
      <div class="question-view">
        <div v-if="loading" class="question-loading">
          <Progress />
        </div>
        <fragment v-else>
          <Question
            v-if="question._id"
            :question="question"
            :comments="comments"
          />
          <div v-if="answers.length" class="question-answers">
            <h2>{{ answers.length }} answers</h2>
            <Answer
              v-for="answer in answers"
              :key="answer._id"
              :answer="answer"
              :comments="comments"
            />
          </div>
        </fragment>
      </div>
    </main>
    <aside>aside</aside>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Question from './Partial/Question'
import Answer from './Partial/Answer'

export default {
  data() {
    return {
      loading: false
    }
  },
  components: {
    Question,
    Answer
  },
  computed: {
    ...mapState({
      question: state => state.questions.question,
      answers: state => state.questions.answers,
      comments: state => state.questions.comments
    })
  },
  methods: {
    reload() {
      this.loading = true
      this.$store
        .dispatch('questions/getQuestion', this.$route.params.questionId)
        .finally(() => {
          this.loading = false
        })
    }
  },
  mounted() {
    this.reload()
  },
  watch: {
    '$route.params.questionId'() {
      this.reload()
    }
  }
}
</script>

<style lang="scss">
.question-view {
  padding: 12px;
}

.question-loading {
  height: calc(100vh - 180px);
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}
</style>
