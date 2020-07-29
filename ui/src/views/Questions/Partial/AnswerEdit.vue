<template>
  <div class="answer-edit">
    <MarkdownEditor
      ref="editor"
      :autofocus="false"
      :error="!!error"
      :disabled="false"
      v-model="body"
    />
    <div v-if="error" class="error-msg">{{ error }}</div>
    <PostEditorActions
      @save="handleSave"
      @cancel="handleCancel"
      :isSaving="isSaving"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import PostCommons from '@/mixins/PostCommons'
import MarkdownEditor from '@/components/Editors/MarkdownEditor.vue'
import { mixins } from 'vue-class-component'
import PostEditorActions from '@/components/PostEditorActions.vue'

@Component({
  components: {
    PostEditorActions,
    MarkdownEditor
  }
})
export default class AnswerEdit extends mixins(PostCommons) {
  @Prop({ type: String, default: '' }) value!: string
  @Prop({ type: Boolean, required: true }) readonly isSaving!: boolean
  @Prop({ type: String, required: false }) readonly error!: string


  private body = this.value

  handleSave() {
    console.log('this value ', this.body)
    this.$emit('save', this.body)
  }

  handleCancel() {
    this.$emit('cancel')
  }

  get editor(): MarkdownEditor {
    return this.$refs.editor as MarkdownEditor
  }

  focus() {
    this.editor.focus()
  }
}
</script>

<style lang="scss"></style>
