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
      <SpinnerButton
        type="submit"
        :loading="posting"
        class="btn btn-primary btn-150"
        >Add Comment</SpinnerButton
      >
    </div>
  </form>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component
export default class CommentForm extends Vue {
  @Prop({ type: Boolean, default: false }) posting!: boolean
  @Prop({ type: Boolean, default: true }) autofocus!: boolean
  @Prop({ type: String, default: '' }) value!: string

  mounted() {
    if (this.autofocus) {
      const input = this.$refs.input as HTMLInputElement
      input.focus()
    }
  }

  handleInput(e: InputEvent) {
    const input = e.target as HTMLInputElement
    this.$emit('input', input.value)
  }

  handleEnter(e: KeyboardEvent) {
    const onMac = window.navigator.platform.startsWith('Mac')
    const needSubmit = (onMac && e.metaKey) || (!onMac && e.ctrlKey)
    if (needSubmit) {
      this.$emit('submit')
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
