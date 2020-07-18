<template>
  <button v-on="$listeners" :disabled="loading">
    <i v-if="loading" class="fas fa-spinner fa-spin"></i>
    <slot v-else></slot>
  </button>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class SpinnerButton extends Vue {
  @Prop({ type: Boolean, default: false }) readonly loading!: boolean
}
</script>
