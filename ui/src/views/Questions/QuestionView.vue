<template>
  <div class="page-layout">
    <main>
      <div class="question-view">
        <div v-if="loading" class="question-loading">
          <Progress />
        </div>
        <fragment v-else>
          <Question v-if="question._id" :question="question" :comments="comments" />
          <div v-if="answers.length" class="question-answers">
            <h2>{{ answersCount }}</h2>
            <Answer
              v-for="answer in answers"
              :key="answer._id"
              :answer="answer"
              :comments="comments"
              :ref="answer._id"
              :class="{flash: answer.flash}"
            />
          </div>
          <!-- Answer form -->
          <hr />
          <h3>Post Your Answer</h3>
          <MarkdownEditor
            ref="editor"
            :autofocus="false"
            :error="!!answerBodyError"
            v-model="answerBody"
          ></MarkdownEditor>
          <div v-if="answerBodyError" class="error-msg">{{ answerBodyError }}</div>
          <div class="preview">
            <h4>Preview</h4>
            <div class="preview-inner">
              <Post :body="answerBody" />
            </div>
          </div>
          <div class="post-form-control">
            <button @click="handlePostAnswer" class="btn btn-primary">Post Answer</button>
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
import Post from '@/components/Post'
import MarkdownEditor from '@/components/Editors/MarkdownEditor'
import { countable } from '@/filters'

export default {
  data() {
    return {
      loading: false,
      answerBody: '',
      answerBodyError: null,
      scrollAwaitedId: null
    }
  },
  components: {
    Question,
    Answer,
    MarkdownEditor,
    Post
  },
  computed: {
    ...mapState({
      question: state => state.questions.question,
      answers: state => state.questions.answers,
      comments: state => state.questions.comments
    }),
    answersCount() {
      return countable(this.answers.length, 'answer', 'answers')
    }
  },
  methods: {
    waitScroll(answerId) {
      this.scrollAwaitedId = answerId
    },
    handlePostAnswer() {
      if (this.answerBody.trim() === '') {
        this.answerBodyError = 'Body can not be empty'
        this.$refs.editor.focus()
        return
      }
      // TODO disable controls, set loading flag
      this.$store
        .dispatch('questions/createAnswer', this.answerBody)
        .then(answerId => {
          this.answerBody = ''
          this.answerBodyError = null
          this.scrollAwaitedId = answerId
        })
        .catch(err => {
          // TODO catch
          console.log(err)
        })
        .finally(() => {
          // TODO reset loading flag, enable controls
        })
    },
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
    },
    answers() {
      if (this.scrollAwaitedId) {
        for (const answer of this.answers) {
          if (answer._id === this.scrollAwaitedId) {
            const id = this.scrollAwaitedId
            this.$nextTick(() => {
              this.$refs[id].scrollIntoView({ block: 'center' })
            })
            this.scrollAwaitedId = null
            break
          }
        }
      }
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
