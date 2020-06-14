<template>
  <router-link :to="userLink" class="user">@{{ username }}</router-link>
</template>

<script>
export default {
  props: {
    username: {
      type: String,
      required: true
    }
  },
  mounted() {
    this.$store.dispatch('users/lazyLoadUser', this.username)
  },
  computed: {
    userLink() {
      return `/users/${this.username}`
    }
  }
}
</script>

<style lang="scss"></style>
