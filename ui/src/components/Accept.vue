<template>
  <div class="answer-accept">
    <a
      class="accept-link"
      href
      :class="{ 'accept-link--green': value, 'accept-link--ro': readonly }"
      @click.prevent="handleAccept"
    >
      <i class="fa fa-check"></i>
    </a>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit } from 'vue-property-decorator'

@Component
export default class Accept extends Vue {
  @Prop({ type: Boolean, required: true }) value!: boolean
  @Prop({ type: Boolean, required: true }) readonly!: boolean

  @Emit('input')
  handleAccept() {
    return !this.value
  }
}
</script>

<style lang="scss">
.answer-accept {
  margin-top: 0.5em;
  font-size: 1.8em;
  text-align: center;
  line-height: 1.1em;

  a.accept-link {
    color: gray;
    text-decoration: none;

    &.accept-link--green {
      color: #494 !important;
    }

    &.accept-link--ro {
      cursor: auto;
    }

    &:hover {
      color: #444;
    }
  }
}
</style>
