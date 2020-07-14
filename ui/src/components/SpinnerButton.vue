<template>
  <button v-on="$listeners" :disabled="loading">
    <i v-if="loading" class="fas fa-spinner fa-spin"></i>
    <slot v-else></slot>
  </button>
</template>

<script>
export default {
  props: {
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="scss">
</style>
