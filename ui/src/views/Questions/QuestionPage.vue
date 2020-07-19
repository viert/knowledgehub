<template>
  <div class="page-layout">
    <main>
      <div class="question-view">
        <div v-if="loading" class="question-loading">
          <Progress />
        </div>
        <fragment v-else>
          <QuestionView
            v-if="question._id"
            :question="question"
            :comments="comments"
          />
          <div v-if="answers.length" class="question-answers">
            <h2>{{ answersCount }}</h2>
            <AnswerView
              v-for="answer in answers"
              :key="answer._id"
              :answer="answer"
              :comments="comments"
              :ref="answer._id"
              :class="{ flash: answer.flash }"
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
          <div v-if="answerBodyError" class="error-msg">{{
            answerBodyError
          }}</div>
          <div class="preview">
            <h4>Preview</h4>
            <div class="preview-inner">
              <Post :body="answerBody" />
            </div>
          </div>
          <div class="post-form-control">
            <button @click="handlePostAnswer" class="btn btn-primary"
              >Post Answer</button
            >
          </div>
        </fragment>
      </div>
    </main>
    <aside>aside</aside>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator'
import QuestionView from './Partial/QuestionView.vue'
import AnswerView from './Partial/AnswerView.vue'
import Post from '@/components/Post.vue'
import MarkdownEditor from '@/components/Editors/MarkdownEditor.vue'
import { namespace } from 'vuex-class'
import { Question, Answer, Comment } from '@/store/types'
import { countable } from '@/filters'

const questions = namespace('questions')

@Component({ components: { QuestionView, AnswerView, MarkdownEditor, Post } })
export default class QuestionPage extends Vue {
  private loading = false
  private answerBody = ''
  private answerBodyError = ''
  private scrollAwaitedId: string | null = null

  @questions.State('question') readonly question!: Question
  @questions.State('answers') readonly answers!: Answer[]
  @questions.State('comments') readonly comments!: Comment[]

  get answersCount() {
    return countable(this.answers.length, 'answer', 'answers')
  }

  get editor() {
    return this.$refs.editor as MarkdownEditor
  }

  waitScroll(answerId: string) {
    this.scrollAwaitedId = answerId
  }

  handlePostAnswer() {
    if (this.answerBody.trim() === '') {
      this.answerBodyError = 'Body can not be empty'
      this.editor.focus()
      return
    }
    // TODO disable controls, set loading flag
    this.$store
      .dispatch('questions/createAnswer', this.answerBody)
      .then(answerId => {
        this.answerBody = ''
        this.answerBodyError = ''
        this.scrollAwaitedId = answerId
      })
      .catch(err => {
        // TODO catch
        console.log(err)
      })
      .finally(() => {
        // TODO reset loading flag, enable controls
      })
  }

  reload() {
    this.loading = true
    this.$store
      .dispatch('questions/getQuestion', this.$route.params.questionId)
      .finally(() => {
        this.loading = false
      })
  }

  mounted() {
    this.reload()
  }

  @Watch('$route.params.questionId')
  onParamsQuestionIdChange() {
    this.reload()
  }

  @Watch('answers')
  onAnswersChange() {
    if (this.scrollAwaitedId) {
      for (const answer of this.answers) {
        if (answer._id === this.scrollAwaitedId) {
          const id = this.scrollAwaitedId
          this.$nextTick(() => {
            const answerElement = this.$refs[id] as HTMLElement
            answerElement.scrollIntoView({ block: 'center' })
          })
          this.scrollAwaitedId = null
          break
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

.question-answers {
  margin-top: 3em;
}
</style>
