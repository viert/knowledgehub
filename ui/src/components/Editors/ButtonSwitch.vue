<template>
  <div class="btn-group">
    <button
      type="button"
      class="btn btn-switch"
      :class="{
        'btn-primary': value[key],
        'btn-outline-secondary': !value[key],
        [`btn-switch--${value[key]}`]: true
      }"
      v-for="key in keys"
      :key="key"
      @click="handleClick(key)"
    >{{key}}</button>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: Object,
      required: true
    }
  },
  computed: {
    keys() {
      return Object.keys(this.value)
    }
  },
  methods: {
    handleClick(key) {
      const value = {
        ...this.value,
        [key]: !this.value[key]
      }
      this.$emit('input', value)
    }
  }
}
</script>

<style lang="scss">
.btn.btn-switch {
  font-family: Montserrat;
  &:before {
    font-family: 'Font Awesome 5 Free';
    font-weight: normal;
    margin-right: 0.5em;
  }

  &.btn-switch--true:before {
    content: '\f14a';
  }
  &.btn-switch--false:before {
    content: '\f0c8';
  }
}
</style>
