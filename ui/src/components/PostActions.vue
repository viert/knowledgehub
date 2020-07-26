<template>
  <div class="post-actions">
    <a @click.prevent href="#">
      edit
    </a>
    <a v-if="!question.deleted" @click.prevent="handleDelete" href="#">
      delete
    </a>
    <a v-else @click.prevent="handleRestore" href="#">
      restore
    </a>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { Answer, Comment, Question, User } from '@/store/types'
const users = namespace('users')
const questions = namespace('questions')

@Component
export default class PostActions extends Vue {
  @users.Getter('me') readonly me!: User
  @questions.State('question') readonly question!: Question
  @questions.State('answers') readonly answers!: Answer[]
  @questions.State('comments') readonly comments!: Comment[]

  handleDelete() {
    this.$store.dispatch('questions/deleteQuestion')
  }

  handleRestore() {
    this.$store.dispatch('questions/restoreQuestion')
  }
}
</script>

<style lang="scss">
.post-actions {
}
</style>
