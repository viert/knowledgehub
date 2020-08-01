<template>
  <div class="event-body">
    Your question <b>{{ event.question_title }}</b> got a new
    <router-link :to="answerLink">answer</router-link> by
    <User :username="event.author_username" :load="true" />
    {{ event.created_at | duration }}
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { QuestionNewAnswerEvent } from '@/store/types'

@Component
export default class NewAnswerEventView extends Vue {
  @Prop({ type: Object, required: true }) event!: QuestionNewAnswerEvent

  get answerLink() {
    return `/questions/${this.event.question_human_readable_id}?answer=${this.event.answer_id}&dismiss=${this.event._id}`
  }
}
</script>
