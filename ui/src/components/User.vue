<template>
  <router-link :to="userLink" class="user"
    >@{{ username
    }}<div
      class="user--moderator"
      v-if="moderator"
      :title="'@' + username + ' is moderator'"
      ><i class="fas fa-sun"></i>
    </div>
  </router-link>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { namespace } from 'vuex-class'

const users = namespace('users')

@Component
export default class User extends Vue {
  @Prop({ type: String, required: true }) readonly username!: string
  @Prop({ type: Boolean, default: true }) readonly load!: boolean
  @Prop({ type: String, default: null }) readonly overrideLink!: string | null

  @users.Getter('user') getUser!: (username: string) => User

  mounted() {
    if (this.load) this.$store.dispatch('users/lazyLoadUser', this.username)
  }

  get moderator(): boolean {
    const user = this.getUser(this.username)
    return (user && user.moderator) || false
  }

  get userLink() {
    if (this.overrideLink) return this.overrideLink
    return `/users/${this.username}`
  }
}
</script>

<style lang="scss">
.user {
  position: relative;
  white-space: pre;
  .user--moderator {
    position: relative;
    display: inline-block;
    top: -7px;
    font-size: 0.7em;
    color: #3377cc;
  }
}
</style>
