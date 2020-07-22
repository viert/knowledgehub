<template>
  <li ref="root" class="comment">
    <div class="comment-voter">
      <Voter
        :mini="true"
        @input="handleVote"
        :points="comment.points"
        :value="comment.my_vote"
      />
    </div>
    <div class="comment-body" :class="{ flash: comment.flash }">
      <Post :body="comment.body" :strict="true" :inline="true" />&mdash;
      <User :username="author.username" />
      {{ comment.created_at | duration }}
    </div>
  </li>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import Post from '@/components/Post.vue'
import PostCommons from '@/mixins/PostCommons'
import { Comment } from '@/store/types'
import { mixins } from 'vue-class-component'

@Component({ components: { Post } })
export default class CommentView extends mixins(PostCommons) {
  @Prop({ type: Object, required: true }) readonly comment!: Comment

  handleVote(value: 1 | 0) {
    this.$store.dispatch('questions/voteComment', {
      commentId: this.comment._id,
      value
    })
  }

  get author() {
    return this.getUser(this.comment.author_id)
  }
}
</script>

<style lang="scss">
li.comment {
  display: flex;
  border-top: 1px solid #cccccc;
  padding: 8px 0;

  .comment-voter {
    min-width: 32px;
  }

  .comment-body {
    flex-grow: 1;
    font-size: 0.9em;
  }
}
</style>
