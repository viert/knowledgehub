<template>
  <div
    class="tag-editor"
    :class="{ 'tag-editor--focused': focused, 'tag-editor--error': error }"
    @click="focus()"
  >
    <tag
      v-for="tag in tags"
      :name="tag"
      :key="tag"
      :cross="true"
      :expandable="false"
      @close="removeTag(tag)"
    />
    <input
      ref="tagInput"
      type="text"
      class="tag-editor_input"
      :placeholder="placeholder"
      :value="value"
      :size="size"
      @input="editorInput"
      @keydown.enter.prevent="addTag"
      @keydown.space.prevent="addTag"
      @keydown.tab="tabHandler"
      @keydown.delete="backspaceHandler"
      @focus="focused = true"
      @blur="onBlur"
    />
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component
export default class TagEditor extends Vue {
  @Prop({ type: Array, default: () => [] }) tags!: string[]
  @Prop({ type: Boolean, default: false }) error!: boolean

  private focused = false
  private value = ''
  private size = 5

  get placeholder() {
    if (!this.tags.length) {
      return 'Add a tag...'
    }
    return null
  }

  focus() {
    const input = this.$refs.tagInput as HTMLInputElement
    input.focus()
  }

  onBlur(e: Event) {
    this.focused = false
    this.addTag(e)
  }

  removeTag(tagName: string) {
    this.$emit('remove', tagName)
  }

  addTag(e: Event) {
    const input = e.target as HTMLInputElement
    const tag = input.value.trim()
    this.value = ''
    this.size = 5
    if (tag.length === 0) return
    if (this.tags.find(i => i === tag)) return
    this.$emit('add', tag)
  }

  tabHandler(e: KeyboardEvent) {
    const input = e.target as HTMLInputElement
    if (input.value.length > 0) {
      e.preventDefault()
      this.addTag(e)
    }
  }

  backspaceHandler(e: KeyboardEvent) {
    const input = e.target as HTMLInputElement
    if (input.value.length === 0) {
      e.preventDefault()
      const lastTag = this.tags[this.tags.length - 1]
      this.removeTag(lastTag)
    }
  }

  editorInput(e: Event) {
    const input = e.target as HTMLInputElement
    const { value, size } = input
    const targetSize = value.length + 5
    let newSize = targetSize
    if (targetSize > size) {
      const inputWidth = input.clientWidth
      const parentWidth = input.parentElement!.clientWidth
      if (inputWidth + 48 > parentWidth) {
        newSize = size
      }
    }
    this.value = value
    this.size = newSize
  }
}
</script>

<style lang="scss">
.tag-editor {
  min-height: 38px;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 6px 12px 2px;
  background-color: white;
  cursor: text;
  transition: border-color 0.15s linear, box-shadow 0.15s linear;
}

.tag-editor--error {
  border-color: #c00;
}

.tag-editor--focused {
  box-shadow: 0 0 0 0.2rem rgba(50, 93, 136, 0.25);
  border-color: #6f9dca;
}

.tag-editor--error.tag-editor--focused {
  border-color: #c00;
  box-shadow: 0 0 0 0.2rem rgba(176, 50, 50, 0.25);
}

.tag-editor_input {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  display: inline-block;
  background-color: transparent;
  padding: 0;
}

.tag-editor .tag {
  cursor: default;
  display: inline-block;
  padding: 1px 8px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  margin-right: 4px;
  margin-bottom: 3px;
  overflow-wrap: normal;
  line-height: 1.5em;
  position: relative;
  top: -1px;
}
</style>
