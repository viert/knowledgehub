<template>
  <div class="answer">
    <div class="answer-post">
      <div class="answer-vote">
        <Voter @input="handleVote" :points="answer.points" :value="answer.my_vote" />
        <Accept :readonly="!isMyQuestion" :value="answer.accepted" @input="handleAccept" />
      </div>
      <div class="answer-body">
        <Post :body="answer.body" />
        <div class="answer-meta">
          <div class="answer-author">
            <AuthorCard action="Answered" :author="author" :askedAt="answer.created_at" />
          </div>
        </div>
        <ul class="comments-section">
          <CommentsList :parentId="answer._id" :comments="selfComments" />
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Post from '@/components/Post'
import CommentsList from './CommentsList'
import AuthorCard from './AuthorCard'
import Accept from '@/components/Accept'

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
    CommentsList,
    AuthorCard,
    Accept
  },
  methods: {
    handleVote(value) {
      this.$store.dispatch('questions/voteAnswer', {
        answerId: this.answer._id,
        value
      })
    },
    handleAccept(value) {
      if (this.answer.accepted) {
        this.$store.dispatch('questions/revokeAnswer', this.answer._id)
      } else {
        this.$store.dispatch('questions/acceptAnswer', this.answer._id)
      }
    }
  },
  computed: {
    ...mapGetters({
      isMyQuestion: 'questions/isMyQuestion'
    }),
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
