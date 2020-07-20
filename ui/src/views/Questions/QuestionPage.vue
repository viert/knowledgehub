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
          <AnswerForm
            v-if="me"
            v-model="answerBody"
            :error="answerBodyError"
            @submit="handlePostAnswer"
          />
          <SigninBanner v-else message="Sign in to post answers" />
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

import MarkdownEditor from '@/components/Editors/MarkdownEditor.vue'
import AnswerForm from '@/components/Editors/AnswerForm.vue'
import SigninBanner from '@/components/SignIn/SigninBanner.vue'

import { namespace } from 'vuex-class'
import { countable } from '@/filters'
import { Question, Answer, Comment, User } from '@/store/types'

const questions = namespace('questions')
const users = namespace('users')

@Component({
  components: {
    QuestionView,
    AnswerView,
    MarkdownEditor,
    AnswerForm,
    SigninBanner
  }
})
export default class QuestionPage extends Vue {
  private loading = true
  private answerBody = ''
  private answerBodyError = ''

  @questions.State('question') readonly question!: Question
  @questions.State('answers') readonly answers!: Answer[]
  @questions.State('comments') readonly comments!: Comment[]
  @users.Getter('me') readonly me!: User

  get answersCount() {
    return countable(this.answers.length, 'answer', 'answers')
  }

  get editor() {
    return this.$refs.editor as MarkdownEditor
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
        this.scrollToAnswerSoon(answerId)
      })
      .catch(err => {
        // TODO catch
        console.log(err)
      })
      .finally(() => {
        // TODO reset loading flag, enable controls
      })
  }

  scrollToAnswerSoon(answerId: string) {
    this.$nextTick(() => {
      const answerElement = this.$refs[answerId] as AnswerView[]
      answerElement[0].scrollIntoView()
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
    if (!this.me) {
      this.$store.commit('users/setSigninOrigin', this.$route.fullPath)
    }
  }

  @Watch('$route.params.questionId')
  onParamsQuestionIdChange() {
    this.reload()
  }
}
</script>

<style lang="scss">
.question-view {
  padding: 12px;

  .signin {
    h3 {
      margin-bottom: 1em;
    }
    padding: 50px;
    background-color: #f9f9f9;
    border: 1px solid #cccccc;
  }
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
