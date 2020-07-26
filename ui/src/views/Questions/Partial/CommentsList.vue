<template>
  <div class="comments-section">
    <ul class="comments-list">
      <CommentView
        v-for="comment in comments"
        :key="comment._id"
        :comment="comment"
      />
    </ul>
    <CommentForm
      v-model="commentBody"
      @submit="handlePostComment"
      :posting="commentPostRequestInProgress"
      @close="formOpened = false"
      v-if="formOpened"
    />
    <a v-else-if="me" @click.prevent="formOpened = true" href="#">
      add a comment
    </a>

    <router-link to="/signin" v-else>sign in to add a comment</router-link>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import CommentView from './CommentView.vue'
import CommentForm from '@/components/Editors/CommentForm.vue'
import { Comment, User } from '@/store/types'
import { namespace } from 'vuex-class'

const users = namespace('users')

@Component({ components: { CommentView, CommentForm } })
export default class CommentsList extends Vue {
  @Prop({ type: Array, default: () => [] }) readonly comments!: Comment[]
  @Prop({ type: String, required: true }) readonly parentId!: string
  @users.Getter('me') readonly me!: User

  private formOpened = false
  private commentBody = ''
  private commentPostRequestInProgress = false

  handlePostComment() {
    this.commentPostRequestInProgress = true
    const payload = {
      parentId: this.parentId,
      body: this.commentBody
    }

    this.$store
      .dispatch('questions/createComment', payload)
      .then(() => {
        this.commentBody = ''
        this.formOpened = false
      })
      .finally(() => {
        this.commentPostRequestInProgress = false
      })
  }
}
</script>

<style lang="scss">
ul.comments-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
</style>
