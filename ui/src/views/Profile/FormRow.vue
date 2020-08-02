<template>
  <div class="form-group row">
    <label :for="id" class="col-sm-3 text-right col-form-label">{{
      label
    }}</label>
    <div class="col-sm-9">
      <slot v-if="hasChildren"></slot>
      <input
        v-else
        type="text"
        class="form-control"
        :id="id"
        :disabled="disabled"
        :placeholder="label"
        :value="value"
        :readonly="readonly"
        :class="{ 'form-control--readonly': readonly }"
        @input="$emit('input', $event.target.value)"
      />
      <div class="input-info"><slot name="info"></slot></div>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component
export default class FormRow extends Vue {
  @Prop({ type: String, required: true }) readonly label!: string
  @Prop({ type: String }) readonly value!: string
  @Prop({ type: Boolean, default: false }) readonly readonly!: boolean
  @Prop({ type: Boolean, default: false }) readonly disabled!: boolean

  get id() {
    return this.label.toLowerCase()
  }

  get hasChildren() {
    return !!this.$slots.default
  }
}
</script>

<style lang="scss">
.form-control.form-control--readonly {
  background: white;
  border: transparent;
  outline: none;
  box-shadow: none;
}

.input-info {
  color: gray;
  font-size: 0.8em;
}
</style>
