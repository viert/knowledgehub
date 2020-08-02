<template>
  <div class="page-layout">
    <main>
      <div class="question-view">
        <div v-if="isLoading" class="question-loading">
          <Progress />
        </div>
        <div v-else-if="notFound" class="not-found">
          <h2>404 Not Found</h2>
          <p>
            Looks like the post you're trying to reach does not exist.<br />
            Check your link once again, or do some searching using the search
            field on the top of the page.
          </p>
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
            ref="editor"
            v-model="answerBody"
            :error="answerBodyError"
            :isSaving="isSaving"
            @submit="handlePostAnswer"
          />
          <SigninBanner v-else message="Sign in to post answers" />
        </fragment>
      </div>
    </main>
    <aside>
      <EventsBlock />
    </aside>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator'

import QuestionView from './Partial/QuestionView.vue'
import AnswerView from './Partial/AnswerView.vue'

import AnswerForm from '@/components/Editors/AnswerForm.vue'
import SigninBanner from '@/components/SignIn/SigninBanner.vue'
import EventsBlock from '@/views/Events/EventsBlock.vue'

import { namespace } from 'vuex-class'
import { countable } from '@/filters'
import { Question, Answer, Comment, User } from '@/store/types'

const questions = namespace('questions')
const users = namespace('users')

@Component({
  components: {
    QuestionView,
    AnswerView,
    AnswerForm,
    SigninBanner,
    EventsBlock
  }
})
export default class QuestionPage extends Vue {
  private isLoading = true
  private isSaving = false
  private answerBody = ''
  private answerBodyError = ''
  private notFound = false

  @questions.State('question') readonly question!: Question
  @questions.State('answers') readonly answers!: Answer[]
  @questions.State('comments') readonly comments!: Comment[]
  @users.Getter('me') readonly me!: User

  mounted() {
    this.reload()
    if (!this.me) {
      this.$store.commit('users/setSigninOrigin', this.$route.fullPath)
    }
  }

  get answersCount() {
    return countable(this.answers.length, 'answer', 'answers')
  }

  get editor() {
    return this.$refs.editor as AnswerForm
  }

  handlePostAnswer() {
    if (this.answerBody.trim() === '') {
      this.answerBodyError = 'Body can not be empty'
      this.editor.focus()
      return
    }
    this.isSaving = true
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
        this.isSaving = false
      })
  }

  scrollToAnswerSoon(answerId: string) {
    this.$nextTick(() => {
      const answerElement = this.$refs[answerId] as AnswerView[]
      answerElement[0].scrollIntoView()
    })
  }

  reload() {
    this.isLoading = true
    this.notFound = false
    this.$store
      .dispatch('questions/getQuestion', this.$route.params.questionId)
      .catch(err => {
        if (err.status === 404) {
          this.notFound = true
        }
      })
      .finally(() => {
        this.isLoading = false
      })
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
