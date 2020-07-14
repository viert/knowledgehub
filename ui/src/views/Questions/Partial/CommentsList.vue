<template>
  <div class="comments-section">
    <ul class="comments-list">
      <Comment v-for="comment in comments" :key="comment._id" :comment="comment" />
    </ul>
    <CommentForm
      v-model="commentBody"
      @submit="handlePostComment"
      :posting="commentPostRequest"
      @close="formOpened=false"
      v-if="formOpened"
    />
    <a v-else @click.prevent="formOpened=true" href="#">add a comment</a>
  </div>
</template>

<script>
import Comment from './Comment'
import CommentForm from '@/components/Editors/CommentForm'

export default {
  components: {
    Comment,
    CommentForm
  },
  props: {
    comments: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      formOpened: false,
      commentBody: '',
      commentPostRequest: false
    }
  },
  methods: {
    handlePostComment() {
      this.commentPostRequest = true
      this.$store
        .dispatch('questions/createQuestionComment', this.commentBody)
        .then(() => {
          this.commentBody = ''
          this.formOpened = false
        })
        .finally(() => {
          this.commentPostRequest = false
        })
    }
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
