<template>
  <div class="page-layout">
    <main v-if="loggedIn">
      <div class="ask">
        <h3 class="page-title">Ask Question</h3>
        <input
          placeholder="Set a title..."
          ref="title"
          class="form-control form-control-lg"
          :class="{'is-invalid': !!titleError}"
          type="text"
          v-model="title"
        />
        <div v-if="titleError" class="error-msg">{{ titleError }}</div>
        <MarkdownEditor ref="editor" :autofocus="false" :error="!!bodyError" v-model="body"></MarkdownEditor>
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
        <div class="post-control">
          <button @click="handleSave" class="btn btn-primary">Post Question</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import Api from '@/api'
import MarkdownEditor from '@/components/Editors/MarkdownEditor'
import TagEditor from '@/components/Editors/TagEditor'
import Post from '@/components/Post'
import RequireAuth from '@/mixins/RequireAuth'

export default {
  data() {
    return {
      tags: [],
      body: '',
      title: '',
      tagsError: null,
      bodyError: null,
      titleError: null
    }
  },
  mixins: [RequireAuth],
  components: {
    MarkdownEditor,
    TagEditor,
    Post
  },
  methods: {
    addTag(tag) {
      this.tags = [...this.tags, tag]
      this.tagsError = null
    },
    removeTag(tag) {
      this.tags = this.tags.filter(item => item !== tag)
    },
    handleSave() {
      if (this.title.trim() === '') {
        this.titleError = 'Title can not be empty'
        this.$refs.title.focus()
        return
      }
      if (this.body.trim() === '') {
        this.bodyError = 'Body can not be empty'
        this.$refs.editor.focus()
        return
      }
      if (!this.tags.length) {
        this.tagsError = 'Please define at least one tag'
        this.$refs.tagEditor.focus()
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
  },
  watch: {
    ready(value) {
      if (value) {
        this.$refs.title.focus()
      }
    },
    body(nv) {
      if (nv !== '') this.bodyError = null
    }
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

.post-control {
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
