<template>
  <div class="form-group row">
    <label :for="id" class="col-sm-3 text-right col-form-label">{{label}}</label>
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
        :class="{'form-control--readonly': readonly }"
        @input="$emit('input', $event.target.value)"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      required: true
    },
    value: {
      type: String,
      default: ''
    },
    readonly: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    id() {
      return this.label.toLowerCase()
    },
    hasChildren() {
      return !!this.$slots.default
    }
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
</style>
