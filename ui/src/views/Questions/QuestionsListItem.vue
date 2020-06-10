<template>
  <li class="question-list_list-item">
    <div class="question-list_list-item_userpic">
      <UserPic v-if="author" :url="author.avatar_url" />
    </div>
    <div class="question-list_list-item_title">
      <h4>
        <router-link :to="questionLink">{{ question.title }}</router-link>
      </h4>
      <div class="question-list_list-item_meta">
        <div class="question-list_list-item_tags">
          <Tag v-for="tag in question.tags" :key="tag" :name="tag" />
        </div>
        <div class="question-list_list-item_date">active {{ question.last_activity_at | duration }}</div>
      </div>
    </div>
    <div class="question-list_list-item_counters">
      <Counter :value="question.points" single="vote" plural="votes" />
      <Counter
        :value="question.answers_count"
        single="answer"
        plural="answers"
        :type="answerCounterType"
      />
      <Counter :value="question.views_count" single="view" plural="views" />
    </div>
  </li>
</template>

<script>
import UserPic from '@/components/UserPic'
import Counter from '@/components/Counter'

export default {
  components: {
    UserPic,
    Counter
  },
  props: {
    question: {
      type: Object,
      required: true
    }
  },
  computed: {
    questionLink() {
      return `/questions/${this.question._id}`
    },
    answerCounterType() {
      if (this.question.answers_count === 0) return ''
      if (this.question.has_accepted_answer) return 'maxgreen'
      return 'green'
    },
    author() {
      return this.$store.getters['users/user'](this.question.author_id)
    }
  }
}
</script>

<style lang="scss">
.question-list_list-item {
  display: flex;
  width: 100%;
  margin-bottom: 24px;

  &_userpic {
    min-width: 52px;
    margin-right: 8px;
  }

  &_title {
    flex-grow: 1;
    h4 {
      font-weight: bold;
      font-size: 1.3em;
      margin-right: 8px;
      a {
        color: black;
        text-decoration: none;
      }
    }
  }

  &_counters {
    min-width: 196px;
    display: flex;
    justify-content: space-between;
  }

  &_meta {
    display: flex;
    justify-content: space-between;
  }

  &_date {
    font-size: 0.85em;
  }
}
</style>
