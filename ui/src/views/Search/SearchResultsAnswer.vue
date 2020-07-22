<template>
  <li class="answer">
    <h5>
      <router-link :to="questionLink">
        A: {{ item.question_title }}
      </router-link>
    </h5>
    <div class="answer-body">
      <p>{{ item.body }}</p>
      <div class="answer-meta">
        <div class="answer-tags">
          <Tag v-for="tag in item.tags" :key="tag" :name="tag" />
        </div>
        <div class="answer-author">
          Answered {{ item.created_at | duration }} by
          <User :username="author.username" />
        </div>
      </div>
    </div>
  </li>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import { Answer } from '@/store/types'
import { mixins } from 'vue-class-component'
import PostCommons from '@/mixins/PostCommons'

@Component
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
