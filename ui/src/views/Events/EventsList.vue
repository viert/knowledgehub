<template>
  <ul class="events-list">
    <li class="events-list_item" v-for="event in events" :key="event._id">
      <NewCommentEventView
        v-if="event.type === 'post_new_comment_event'"
        :event="event"
      />
      <div class="event-dismiss">
        <a href="#" @click.prevent="handleDismiss(event._id)">
          <i class="fas fa-trash"></i>
        </a>
      </div>
    </li>
  </ul>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { AnyEvent, MaxPage } from '@/store/types'
import NewCommentEventView from './Items/NewCommentEventView.vue'

const events = namespace('events')
@Component({ components: { NewCommentEventView } })
export default class EventsList extends Vue {
  @events.State('eventsList') events!: AnyEvent[]
  @events.State('page') readonly page!: number
  @events.State('totalPages') readonly totalPages!: number
  @events.State('loading') readonly loading!: boolean

  load(page: number) {
    this.$store.dispatch('events/loadEvents', page).catch(err => {
      if (err instanceof MaxPage) {
        this.pageChanged(err.maxPage)
      }
    })
  }

  handleDismiss(eventId: string) {
    this.$store.dispatch('events/dismiss', eventId)
  }

  pageChanged(page: number) {
    this.load(page)
  }

  mounted() {
    this.load(1)
  }
}
</script>

<style lang="scss">
.events-list {
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 0.9em;
  .events-list_item {
    padding: 0.7em 8px;
    display: flex;

    &:hover {
      background-color: #eeeeee;
    }

    &:not(:last-child) {
      border-bottom: 1px solid #eeeeee;
    }

    .event-body {
      flex-grow: 1;
    }
    .event-dismiss {
      font-size: 0.8em;
      width: 12px;
      min-width: 12px;
      text-align: right;
      a {
        color: gray;
        &:hover {
          color: black;
        }
      }
    }
  }
}
</style>
