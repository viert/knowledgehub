<template>
  <div class="answer">
    <div class="answer-post">
      <div class="answer-vote">
        <Voter
          @input="handleVote"
          :points="answer.points"
          :value="answer.my_vote"
        />
        <Accept
          :readonly="!isMyQuestion"
          :value="answer.accepted"
          @input="handleAccept"
        />
      </div>
      <div class="answer-body">
        <Post :body="answer.body" />
        <div class="answer-meta">
          <div class="answer-author">
            <AuthorCard
              action="Answered"
              :author="author"
              :askedAt="answer.created_at"
            />
          </div>
        </div>
        <ul class="comments-section">
          <CommentsList :parentId="answer._id" :comments="selfComments" />
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import PostCommons from './PostCommons'
import Post from '@/components/Post.vue'
import Accept from '@/components/Accept.vue'
import CommentsList from './CommentsList.vue'
import AuthorCard from './AuthorCard.vue'
import { Answer, Comment } from '@/store/types'
import { mixins } from 'vue-class-component'

@Component({ components: { Post, CommentsList, AuthorCard, Accept } })
export default class AnswerView extends mixins(PostCommons) {
  @Prop({ type: Object, required: true }) readonly answer!: Answer
  @Prop({ type: Array, default: () => [] }) readonly comments!: Comment[]

  handleVote(value: 1 | 0 | -1) {
    this.$store.dispatch('questions/voteAnswer', {
      answerId: this.answer._id,
      value
    })
  }

  handleAccept() {
    if (this.answer.accepted) {
      this.$store.dispatch('questions/revokeAnswer', this.answer._id)
    } else {
      this.$store.dispatch('questions/acceptAnswer', this.answer._id)
    }
  }

  get selfComments() {
    return this.comments.filter(c => c.parent_id === this.answer._id)
  }

  get author() {
    return this.getUser(this.answer.author_id)
  }
}
</script>

<style lang="scss">
.answer {
  border-top: 1px solid #cccccc;
  padding-top: 20px;
}
</style>
