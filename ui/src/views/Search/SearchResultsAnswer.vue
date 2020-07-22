<template>
  <li class="answer">
    <div class="answer-contents">
      <div class="answer-body">
        <h5>
          <router-link :to="questionLink">
            A: {{ item.question_title }}
          </router-link>
        </h5>
        <p>{{ item.body }}</p>
      </div>
      <div class="answer-counters">
        <Counter :value="item.points" single="vote" plural="votes" />
      </div>
    </div>
    <div class="answer-meta">
      <div class="answer-tags">
        <Tag v-for="tag in item.tags" :key="tag" :name="tag" />
      </div>
      <div class="answer-author">
        Answered {{ item.created_at | duration }} by
        <User :username="author.username" />
      </div>
    </div>
  </li>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import { Answer } from '@/store/types'
import { mixins } from 'vue-class-component'
import PostCommons from '@/mixins/PostCommons'
import Counter from '@/components/Counter.vue'

@Component({ components: { Counter } })
export default class SearchResultsQuestion extends mixins(PostCommons) {
  @Prop({ type: Object, required: true }) readonly item!: Answer

  get author() {
    return this.getUser(this.item.author_id)
  }

  get questionLink() {
    return `/questions/${this.item.parent_id}`
  }
}
</script>

<style lang="scss">
li.answer {
  .answer-contents {
    display: flex;
    .answer-body {
      flex-grow: 1;
    }
    .answer-counters {
      display: flex;
      width: 150px;
      min-width: 150px;
      justify-content: flex-end;
    }
  }
}
</style>
