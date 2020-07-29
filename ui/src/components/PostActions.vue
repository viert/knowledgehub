<template>
  <div class="post-actions">
    <a @click.prevent href="#">
      edit
    </a>
    <a v-if="!isDeleted" @click.prevent="handleDelete" href="#">
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
  @Prop({ type: String, required: true }) readonly view!: string
  @users.Getter('me') readonly me!: User
  @questions.State('question') readonly question!: Question
  @Prop({ type: Object, required: false }) readonly answer!: Answer
  @Prop({ type: String, required: false }) readonly parentId!: string

  handleDelete() {
    switch (this.view) {
      case 'question':
        this.$store.dispatch('questions/deleteQuestion')
        break
      case 'answer':
        this.$store.dispatch('questions/deleteAnswer', this.parentId)
        break
      default:
        console.error(
          'Err: default case, no action in handleDelete of PostActions'
        )
    }
  }

  get isDeleted() {
    let isDeleted = false
    switch (this.view) {
      case 'question':
        isDeleted = this.question.deleted
        break
      case 'answer':
        isDeleted = this.answer.deleted
        break
    }
    return isDeleted
  }

  handleRestore() {
    switch (this.view) {
      case 'question':
        this.$store.dispatch('questions/restoreQuestion')
        break
      case 'answer':
        this.$store.dispatch('questions/restoreAnswer', this.parentId)
        break
      default:
        console.error(
          'Err: default case, no action in handleDelete of PostActions'
        )
    }
  }
}
</script>

<style lang="scss">
.post-actions {
}
</style>
