<template>
  <div class="aside-section events-section">
    <h4>Events</h4>
    <div v-if="me">
      <EventsList />
    </div>
    <div v-else class="events-signin">
      Please <router-link to="/signin">Sign in</router-link> to see your events
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { User } from '@/store/types'
import EventsList from './EventsList.vue'

const users = namespace('users')
@Component({ components: { EventsList } })
export default class EventsBlock extends Vue {
  @users.Getter('me') readonly me!: User
}
</script>

<style lang="scss">
.events-signin {
  padding: 20px 0;
  a {
    font-weight: bold;
  }
}
</style>
