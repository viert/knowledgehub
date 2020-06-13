<template>
  <fragment>
    <router-link v-if="user" :to="userLink" class="user">@{{ username }}</router-link>
  </fragment>
</template>

<script>
export default {
  props: {
    username: {
      type: String,
      required: true
    }
  },
  computed: {
    user() {
      const user = this.$store.getters['users/user'](this.username)
      if (!user) {
        this.$store.dispatch('users/lazyLoadUser', this.username)
      }
      return user
    },
    userLink() {
      return `/users/${this.username}`
    }
  }
}
</script>

<style lang="scss">
</style>
