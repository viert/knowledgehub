<template>
  <div class="event-body">
    You were mentioned in
    <router-link :to="postLink">{{ postType }}</router-link>
    by
    <User :username="event.author_username" :load="true" />
    {{ event.created_at | duration }}
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { MentionEvent } from '@/store/types'

@Component
export default class MentionEventView extends Vue {
  @Prop({ type: Object, required: true }) event!: MentionEvent

  get postType() {
    switch (this.event.post_type) {
      case 'question':
        return 'a question'
      case 'answer':
        return 'an answer'
      default:
        return 'a comment'
    }
  }

  get postLink() {
    if (this.event.post_type === 'question')
      return `/questions/${this.event.root_id}?dismiss=${this.event._id}`
    return `/questions/${this.event.root_id}?${this.event.post_type}=${this.event.post_id}&dismiss=${this.event._id}`
  }
}
</script>
