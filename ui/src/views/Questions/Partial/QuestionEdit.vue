<template>
  <div class="page-layout">
  </div>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator'

import QuestionView from './Partial/QuestionView.vue'
import AnswerView from './Partial/AnswerView.vue'

import AnswerForm from '@/components/Editors/AnswerForm.vue'

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
  }
})
export default class QuestionEdit extends Vue {
  private loading = true
  private answerBody = ''
  private answerBodyError = ''
  private isSaving = false

  @questions.State('question') readonly question!: Question
  @questions.State('answers') readonly answers!: Answer[]
  @questions.State('comments') readonly comments!: Comment[]
  @users.Getter('me') readonly me!: User
}
</script>

<style lang="scss"></style>
