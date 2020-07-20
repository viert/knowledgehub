<template>
  <div ref="root" class="question">
    <h2>{{ question.title }}</h2>
    <hr />
    <div class="question-post">
      <div class="question-vote">
        <Voter
          @input="handleVote"
          :points="question.points"
          :value="question.my_vote"
        />
      </div>
      <div class="question-body">
        <Post :body="question.body" />
        <div class="question-meta">
          <div class="question-tags">
            <Tag v-for="tag in question.tags" :key="tag" :name="tag" />
          </div>
          <div class="question-author">
            <AuthorCard
              action="Asked"
              :author="author"
              :askedAt="question.created_at"
            />
          </div>
        </div>
        <CommentsList :parentId="question._id" :comments="selfComments" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import PostCommons from './PostCommons'
import { mixins } from 'vue-class-component'
import Post from '@/components/Post.vue'
import CommentsList from './CommentsList.vue'
import AuthorCard from './AuthorCard.vue'
import { Question, Comment } from '@/store/types'

@Component({ components: { Post, CommentsList, AuthorCard } })
export default class QuestionView extends mixins(PostCommons) {
  @Prop({ type: Object, required: true }) question!: Question
  @Prop({ type: Array, default: () => [] }) readonly comments!: Comment[]

  handleVote(value: 1 | 0 | -1) {
    this.$store.dispatch('questions/voteQuestion', value)
  }

  get selfComments() {
    return this.comments.filter(c => c.parent_id === this.question._id)
  }

  get author() {
    return this.getUser(this.question.author_id)
  }
}
</script>

<style lang="scss">
.question,
.answer {
  h2 {
    font-weight: bold;
  }

  &-post {
    display: flex;
  }
  &-vote {
    min-width: 60px;
    width: 60px;
    margin-right: 12px;
  }
  &-body {
    flex-grow: 1;
  }

  &-meta {
    display: flex;
    justify-content: flex-end;
  }

  &-tags {
    flex-grow: 1;
  }
}
</style>