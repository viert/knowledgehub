<template>
  <div class="answer">
    <div class="answer-post">
      <div class="answer-vote">
        <Voter :points="answer.points" :value="answer.my_vote" />
      </div>
      <div class="answer-body">
        <Post :body="answer.body" />
        <div class="answer-meta">
          <div class="answer-author">
            <AuthorCard action="Answered" :author="author" :askedAt="answer.created_at" />
          </div>
        </div>
        <ul class="comments-section">
          <Comment v-for="comment in selfComments" :key="comment._id" :comment="comment" />
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import Post from '@/components/Post'
import Comment from './Comment'
import AuthorCard from './AuthorCard'

export default {
  props: {
    answer: {
      type: Object,
      required: true
    },
    comments: {
      type: Array,
      default: () => []
    }
  },
  components: {
    Post,
    Comment,
    AuthorCard
  },
  computed: {
    selfComments() {
      return this.comments.filter(c => c.parent_id === this.answer._id)
    },
    author() {
      return this.$store.getters['users/user'](this.answer.author_id)
    }
  }
}
</script>

<style lang="scss">
.answer {
  border-top: 1px solid #cccccc;
  padding-top: 20px;
}
</style>
