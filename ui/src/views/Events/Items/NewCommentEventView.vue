<template>
  <div class="event-body">
    You got a new <router-link :to="commentLink">comment</router-link> by
    <User :username="event.author_username" :load="true" />
    {{ event.created_at | duration }}
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { PostNewCommentEvent } from '@/store/types'

@Component
export default class NewCommentEventView extends Vue {
  @Prop({ type: Object, required: true }) event!: PostNewCommentEvent

  get commentLink() {
    return `/questions/${this.event.root_id}?comment=${this.event.post_id}&dismiss=${this.event._id}`
  }
}
</script>

<style scoped></style>
