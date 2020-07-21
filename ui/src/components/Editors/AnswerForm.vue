<template>
  <div class="answer-form">
    <h3>Post Your Answer</h3>
    <MarkdownEditor
      ref="editor"
      :autofocus="false"
      :error="!!error"
      :disabled="isSaving"
      :value="value"
      @input="$emit('input', $event)"
    />
    <div v-if="error" class="error-msg">{{ error }}</div>
    <div class="preview">
      <h4>Preview</h4>
      <div class="preview-inner">
        <Post :body="value" />
      </div>
    </div>
    <div class="post-form-control">
      <SpinnerButton
        @click="$emit('submit')"
        class="btn btn-primary btn-150"
        type="submit"
        :loading="isSaving"
        >Post Answer</SpinnerButton
      >
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import MarkdownEditor from './MarkdownEditor.vue'
import Post from '@/components/Post.vue'
import { namespace } from 'vuex-class'
import { Question } from '@/store/types'

const questions = namespace('questions')

@Component({ components: { MarkdownEditor, Post } })
export default class AnswerForm extends Vue {
  @Prop({ type: String, default: '' }) readonly value!: string
  @Prop({ type: String, default: '' }) readonly error!: string
  @questions.State('question') readonly question!: Question
  @Prop({ type: Boolean, default: false }) isSaving!: boolean

  get editor(): MarkdownEditor {
    return this.$refs.editor as MarkdownEditor
  }

  focus() {
    this.editor.focus()
  }
}
</script>

<style scoped></style>
