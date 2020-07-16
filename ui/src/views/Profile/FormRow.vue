<template>
  <div class="form-group row">
    <label :for="id" class="col-sm-3 text-right col-form-label">{{label}}</label>
    <div class="col-sm-9">
      <input
        type="text"
        class="form-control"
        :id="id"
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
    }
  },
  computed: {
    id() {
      return this.label.toLowerCase()
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
