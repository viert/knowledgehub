<template>
  <li class="question">
    <h5>
      <router-link :to="questionLink"> Q: {{ item.title }} </router-link>
    </h5>
    <div class="question-body">
      <p>{{ item.body }}</p>
      <div class="question-meta">
        <div class="question-tags">
          <Tag v-for="tag in item.tags" :key="tag" :name="tag" />
        </div>
        <div class="question-author">
          Asked {{ item.created_at | duration }} by
          <User :username="author.username" />
        </div>
      </div>
    </div>
  </li>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import { Question } from '@/store/types'
import PostCommons from '@/mixins/PostCommons'
import { mixins } from 'vue-class-component'

@Component
export default class SearchResultsQuestion extends mixins(PostCommons) {
  @Prop({ type: Object, required: true }) readonly item!: Question

  get author() {
    return this.getUser(this.item.author_id)
  }

  get questionLink() {
    return `/questions/${this.item._id}`
  }
}
</script>
