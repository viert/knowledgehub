<template>
  <div class="question-edit">
    <input
      class="form-control form-control-sm question-edit_title"
      type="text"
      v-model="title"
    />
    <MarkdownEditor
      ref="editor"
      :autofocus="true"
      :error="!!error"
      :disabled="false"
      v-model="body"
      @cancel="handleCancel"
    />
    <div v-if="error" class="error-msg">{{ error }}</div>

    <TagEditor
      ref="tagEditor"
      :tags="tags"
      :error="!!tagsError"
      @add="addTag"
      @remove="removeTag"
    />
    <div v-if="tagsError" class="error-msg">{{ tagsError }}</div>
    <PostEditorActions
      @save="handleSave"
      @cancel="handleCancel"
      :isSaving="isSaving"
      name="question"
    />
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import MarkdownEditor from '@/components/Editors/MarkdownEditor.vue'
import TagEditor from '@/components/Editors/TagEditor.vue'
import { Question } from '@/store/types'
import PostEditorActions from '@/components/PostEditorActions.vue'

@Component({
  components: {
    MarkdownEditor,
    PostEditorActions,
    TagEditor
  }
})
export default class QuestionEdit extends Vue {
  @Prop({ type: Object, required: true }) question!: Question
  @Prop({ type: Boolean, required: true }) readonly isSaving!: boolean

  private body = this.question.body
  private title = this.question.title
  private tags = this.question.tags
  private error: string | null = null
  private tagsError: string | null = null

  get questionEditor() {
    return this.$refs.editor as MarkdownEditor
  }

  get tagEditor() {
    return this.$refs.tagEditor as TagEditor
  }

  handleSave() {
    if (this.body.trim() === '') {
      this.error = 'Body can not be empty'
      this.questionEditor.focus()
      return
    }

    if (!this.tags.length) {
      this.tagsError = 'Please add at least one tag'
      this.tagEditor.focus()
      return
    }

    this.$emit('save', {
      body: this.body,
      title: this.title,
      tags: this.tags
    })
  }

  handleCancel() {
    this.$emit('cancel')
  }

  addTag(tagName: string) {
    this.tags = [...this.tags, tagName]
    this.tagsError = null
  }

  removeTag(tagName: string) {
    this.tags = this.tags.filter(item => item !== tagName)
  }
}
</script>

<style lang="scss">
.question-edit {
  .question-edit_title {
    margin: 10px 0;
  }
  .markdown-editor {
    margin: 10px 0;
  }
}
</style>
