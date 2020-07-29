<template>
  <div class="post-actions">
    <a @click.prevent="handleEdit" href="#">
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
  @users.Getter('me') readonly me!: User
  @questions.State('question') readonly question!: Question
  @Prop({ type: Object, required: false }) readonly answer!: Answer
  @Prop({ type: String, required: false }) readonly parentId!: string
  @Prop({ type: Boolean, required: true }) readonly isDeleted!: boolean

  handleDelete() {
    this.$emit('delete', this.parentId)
  }

  handleRestore() {
    this.$emit('restore', this.parentId)
  }

  handleEdit() {
    this.$emit('edit', this.parentId)
  }
}
</script>

<style lang="scss">
.post-actions {
}
</style>
