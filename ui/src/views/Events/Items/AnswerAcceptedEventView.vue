<template>
  <div class="event-body">
    Your <router-link :to="answerLink">answer</router-link> to question
    <b>{{ event.question_title }}</b> was accepted by
    <User :username="event.accepted_by_username" :load="true" />
    {{ event.created_at | duration }}
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { AnswerAcceptedEvent } from '@/store/types'

@Component
export default class AnswerAcceptedEventView extends Vue {
  @Prop({ type: Object, required: true }) event!: AnswerAcceptedEvent

  get answerLink() {
    return `/questions/${this.event.question_id}?answer=${this.event.answer_id}&dismiss=${this.event._id}`
  }
}
</script>

