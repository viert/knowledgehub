<template>
  <div class="event-body">
    A new question
    <b
      ><router-link :to="questionLink">{{
        event.question_title
      }}</router-link></b
    >
    tagged with
    <span class="tag-list">
      <Tag v-for="tag in event.tags" :key="tag" :name="tag" /> </span
    >was published by
    <User :username="event.author_username" :load="true" />
    {{ event.created_at | duration }}
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { TagNewQuestionEvent } from '@/store/types'

@Component
export default class TagNewQuestionEventView extends Vue {
  @Prop({ type: Object, required: true }) event!: TagNewQuestionEvent

  get tags() {
    return this.event.tags.join(',')
  }

  get questionLink() {
    return `/questions/${this.event.question_human_readable_id}?dismiss=${this.event._id}`
  }
}
</script>
