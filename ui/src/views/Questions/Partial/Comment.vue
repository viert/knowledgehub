<template>
  <li class="comment">
    <div class="comment-voter">
      <Voter :mini="true" :points="comment.points" :value="comment.my_vote" />
    </div>
    <div class="comment-body" :class="{flash: comment.flash}">
      <Post :body="comment.body" :strict="true" :inline="true" />&mdash;
      <User :username="commentAuthor.username" />
      {{ comment.created_at | duration }}
    </div>
  </li>
</template>

<script>
import Post from '@/components/Post'
export default {
  props: {
    comment: {
      type: Object,
      required: true
    }
  },
  components: {
    Post
  },
  computed: {
    commentAuthor() {
      return this.$store.getters['users/user'](this.comment.author_id)
    }
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
