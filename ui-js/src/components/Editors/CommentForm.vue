<template>
  <form @submit.prevent="$emit('submit')" class="comment-form">
    <textarea
      @keydown.enter="handleEnter"
      @keydown.esc="$emit('close')"
      @input="handleInput"
      :disabled="posting"
      :value="value"
      ref="input"
      class="form-control"
    ></textarea>
    <div class="post-form-control">
      <SpinnerButton type="submit" :loading="posting" class="btn btn-primary btn-150">Add Comment</SpinnerButton>
    </div>
  </form>
</template>

<script>
export default {
  props: {
    posting: {
      type: Boolean,
      default: false
    },
    value: {
      type: String,
      default: ''
    },
    autofocus: {
      type: Boolean,
      default: true
    }
  },
  mounted() {
    if (this.autofocus) {
      this.$refs.input.focus()
    }
  },
  methods: {
    handleInput(e) {
      this.$emit('input', e.target.value)
    },
    handleEnter(e) {
      const onMac = window.navigator.platform.startsWith('Mac')
      const needSubmit = (onMac && e.metaKey) || (!onMac && e.ctrlKey)
      if (needSubmit) {
        this.$emit('submit')
      }
    }
  }
}
</script>

<style lang="scss">
.comment-form {
  textarea {
    margin-bottom: 1em;
    height: 80px;
  }
  .post-form-control {
    margin-top: 1em;
  }
}

.btn-150 {
  width: 150px;
}
</style>
