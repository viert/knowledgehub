<template>
  <router-link :to="userLink" class="user">@{{ user.username }}</router-link>
</template>

<script>
export default {
  props: {
    id: {
      type: String,
      required: true
    }
  },
  computed: {
    user() {
      const user = this.$store.getters['users/user'](this.id)
      if (!user) {
        this.$store.dispatch('users/lazyLoadUser', this.id)
      }
      return user
    },
    userLink() {
      const userId = this.user ? this.user.username : this.id
      return `/users/${userId}`
    }
  }
}
</script>

<style lang="scss">
</style>
