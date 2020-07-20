<template>
  <router-link :to="userLink" class="user">@{{ username }}</router-link>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class User extends Vue {
  @Prop({ type: String, required: true }) readonly username!: string
  @Prop({ type: Boolean, default: true }) readonly load!: boolean

  mounted() {
    if (this.load) this.$store.dispatch('users/lazyLoadUser', this.username)
  }

  get userLink() {
    return `/users/${this.username}`
  }
}
</script>
