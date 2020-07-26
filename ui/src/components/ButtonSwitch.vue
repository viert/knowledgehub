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
      >{{ key }}</button
    >
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'


@Component
export default class ButtonSwitch extends Vue {
  @Prop({ type: Object, required: true }) readonly value!: {
    [key: string]: boolean
  }

  get keys() {
    return Object.keys(this.value)
  }

  handleClick(key: string) {
    const value = {
      ...this.value,
      [key]: !this.value[key]
    }
    this.$emit('input', value)
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
