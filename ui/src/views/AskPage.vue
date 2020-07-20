<template>
  <div class="page-layout">
    <main v-if="loggedIn">
      <div class="ask">
        <h3 class="page-title">Ask Question</h3>
        <input
          placeholder="Set a title..."
          ref="title"
          class="form-control form-control-lg"
          :class="{ 'is-invalid': !!titleError }"
          type="text"
          v-model="title"
        />
        <div v-if="titleError" class="error-msg">{{ titleError }}</div>
        <MarkdownEditor
          ref="editor"
          :autofocus="false"
          :error="!!bodyError"
          v-model="body"
        ></MarkdownEditor>
        <div v-if="bodyError" class="error-msg">{{ bodyError }}</div>
        <TagEditor
          ref="tagEditor"
          :tags="tags"
          :error="!!tagsError"
          @add="addTag"
          @remove="removeTag"
        />
        <div v-if="tagsError" class="error-msg">{{ tagsError }}</div>
        <div class="preview">
          <h4>Preview</h4>
          <div class="preview-inner">
            <Post :body="body" />
          </div>
        </div>
        <div class="post-form-control">
          <button @click="handleSave" class="btn btn-primary"
            >Post Question</button
          >
        </div>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { Component, Watch } from 'vue-property-decorator'
import { mixins } from 'vue-class-component'
import RequireAuth from '@/mixins/RequireAuth'

import MarkdownEditor from '@/components/Editors/MarkdownEditor.vue'
import TagEditor from '@/components/Editors/TagEditor.vue'
import Post from '@/components/Post.vue'
import Api from '../api'

@Component({
  components: {
    MarkdownEditor,
    TagEditor,
    Post
  }
})
export default class AskPage extends mixins(RequireAuth) {
  private tags: string[] = []
  private body = ''
  private title = ''
  private tagsError: string | null = null
  private bodyError: string | null = null
  private titleError: string | null = null

  get titleInput() {
    return this.$refs.title as HTMLInputElement
  }

  get markdownEditor() {
    return this.$refs.editor as MarkdownEditor
  }

  get tagEditor() {
    return this.$refs.tagEditor as TagEditor
  }

  addTag(tagName: string) {
    this.tags = [...this.tags, tagName]
    this.tagsError = null
  }

  removeTag(tagName: string) {
    this.tags = this.tags.filter(item => item !== tagName)
  }

  handleSave() {
    if (this.title.trim() === '') {
      this.titleError = 'Title can not be empty'
      this.titleInput.focus()
      return
    }
    if (this.body.trim() === '') {
      this.bodyError = 'Body can not be empty'
      this.markdownEditor.focus()
      return
    }
    if (!this.tags.length) {
      this.tagsError = 'Please define at least one tag'
      this.tagEditor.focus()
      return
    }
    // TODO disable controls, set loading flag
    Api.Questions.Create(this.title, this.body, this.tags)
      .then(response => {
        const questionId = response.data.data._id
        this.$router.replace(`/questions/${questionId}`)
      })
      .catch(() => {
        // TODO enable controls, reset loading flag
      })
  }

  onReady() {
    this.titleInput.focus()
  }

  @Watch('body')
  onBodyChange(newValue: string) {
    console.log('on body change')
    if (newValue !== '') this.bodyError = null
  }
}
</script>

<style lang="scss">
.ask {
  padding: 20px;

  .tag-editor,
  .markdown-editor {
    margin-top: 1.4em;
  }
}

.post-form-control {
  text-align: right;
  margin-top: 2em;
  .btn {
    font-size: 1em;
  }
}

.preview {
  background: #eeeeee;
  padding: 8px;
  margin-top: 1em;
  h4 {
    font-family: Montserrat;
  }
  .preview-inner {
    padding: 8px;
    background: white;
  }
}

.error-msg {
  color: #900;
  font-style: italic;
  font-size: 0.85em;
}
</style>
