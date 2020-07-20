<template>
  <div
    class="cnt"
    :class="{
      'cnt--green': type === 'green',
      'cnt--maxgreen': type === 'maxgreen'
    }"
  >
    <div class="cnt-value">{{ value }}</div>
    <div class="cnt-what">{{ what }}</div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class Counter extends Vue {
  @Prop({ type: Number, required: true }) readonly value!: number
  @Prop({ type: String, required: true }) readonly single!: string
  @Prop({ type: String, required: true }) readonly plural!: string
  @Prop({ type: String, default: '' }) readonly type!: string

  get what() {
    if (this.value % 10 === 1) {
      return this.single
    }
    return this.plural
  }
}
</script>

<style lang="scss">
.cnt {
  width: 60px;
  height: 62px;
  border: 1px solid transparent;
  border-radius: 4px;
  color: #999999;
  padding: 6px;

  &-value {
    text-align: center;
    font-size: 1.6em;
    line-height: 1em;
    font-weight: bold;
  }
  &-what {
    font-size: 0.8em;
    text-align: center;
  }
}

.cnt--green {
  border: 1px solid #77cc77;
  color: #449944;
}

.cnt--maxgreen {
  background-color: #669966;
  color: white;
  border: 1px solid #449944;
}
</style>
