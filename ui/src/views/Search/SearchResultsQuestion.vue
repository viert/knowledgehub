<template>
  <li class="question">
    <div class="question-contents">
      <div class="question-body">
        <h5>
          <router-link :to="questionLink"> Q: {{ item.title }} </router-link>
        </h5>
        <p>{{ item.body }}</p>
      </div>
      <div class="question-counters">
        <Counter
          :value="item.answers_count"
          single="answer"
          plural="answers"
          :type="answerCounterType"
        />
        <Counter :value="item.points" single="vote" plural="votes" />
      </div>
    </div>
    <div class="question-meta">
      <div class="question-tags">
        <Tag v-for="tag in item.tags" :key="tag" :name="tag" />
      </div>
      <div class="question-author">
        Asked {{ item.created_at | duration }} by
        <User :username="author.username" />
      </div>
    </div>
  </li>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import { Question } from '@/store/types'
import PostCommons from '@/mixins/PostCommons'
import { mixins } from 'vue-class-component'
import Counter from '@/components/Counter.vue'

@Component({ components: { Counter } })
export default class SearchResultsQuestion extends mixins(PostCommons) {
  @Prop({ type: Object, required: true }) readonly item!: Question

  get author() {
    return this.getUser(this.item.author_id)
  }

  get questionLink() {
    return `/questions/${this.item._id}`
  }

  get answerCounterType() {
    if (this.item.answers_count === 0) return ''
    if (this.item.has_accepted_answer) return 'maxgreen'
    return 'green'
  }
}
</script>

<style lang="scss">
li.question {
  width: 100%;

  .question-contents {
    display: flex;
    .question-counters {
      display: flex;
      width: 150px;
      min-width: 150px;
      justify-content: flex-end;
    }
    .question-body {
      flex-grow: 1;
    }
  }
}
</style>
