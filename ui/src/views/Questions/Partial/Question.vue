<template>
  <div class="question">
    <h2>{{ question.title }}</h2>
    <hr />
    <div class="question-post">
      <div class="question-vote">
        <Voter :points="question.points" :value="question.my_vote" />
      </div>
      <div class="question-body">
        <Post :body="question.body" />
        <div class="question-meta">
          <div class="question-tags">
            <Tag v-for="tag in question.tags" :key="tag" :name="tag" />
          </div>
          <div class="question-author">
            <AuthorCard action="Asked" :author="author" :askedAt="question.created_at" />
          </div>
        </div>
        <CommentsList :comments="selfComments" />
      </div>
    </div>
  </div>
</template>

<script>
import Post from '@/components/Post'
import CommentsList from './CommentsList'
import AuthorCard from './AuthorCard'

export default {
  props: {
    question: {
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
    CommentsList,
    AuthorCard
  },
  computed: {
    selfComments() {
      return this.comments.filter(c => c.parent_id === this.question._id)
    },
    author() {
      return this.$store.getters['users/user'](this.question.author_id)
    }
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
