<template>
  <div class="markdown-editor">
    <div class="markdown-editor_control_buttons">
      <div class="btn-group">
        <button
          tabindex="-1"
          @click="handleHeader"
          title="Header"
          class="btn-mdctrl"
        >
          <b>h2</b>
        </button>
        <button
          tabindex="-1"
          @click="handleBold"
          title="Bold"
          class="btn-mdctrl"
        >
          <i class="fas fa-bold"></i>
        </button>
        <button
          tabindex="-1"
          @click="handleItalic"
          title="Italic"
          class="btn-mdctrl"
        >
          <i class="fas fa-italic"></i>
        </button>
        <button
          tabindex="-1"
          @click="handleStrike"
          title="Strike-through"
          class="btn-mdctrl"
        >
          <i class="fas fa-strikethrough"></i>
        </button>
        <link-options
          v-if="linkOptionsOpen"
          :initial-title="currentSelection"
          @add="handleAddLink"
          @close="
            linkOptionsOpen = false
            focus()
          "
        />
        <button
          tabindex="-1"
          @click="handleLink"
          title="Add Link"
          class="btn-mdctrl"
        >
          <i class="fas fa-link"></i>
        </button>
        <button
          tabindex="-1"
          @click="handleUnorderedList"
          title="Unordered List"
          class="btn-mdctrl"
        >
          <i class="fas fa-list-ul"></i>
        </button>
        <button
          tabindex="-1"
          @click="handleOrderedList"
          title="Ordered List"
          class="btn-mdctrl"
        >
          <i class="fas fa-list-ol"></i>
        </button>
        <username-picker
          v-if="usernamePickerOpen"
          @add="handleAddUsername"
          @close="
            usernamePickerOpen = false
            focus()
          "
        />
        <button
          tabindex="-1"
          @click="handleUsername"
          title="User"
          class="btn-mdctrl"
        >
          <i class="fas fa-user"></i>
        </button>
        <button
          tabindex="-1"
          @click="handleQuote"
          title="Blockquote"
          class="btn-mdctrl"
        >
          <i class="fas fa-quote-right"></i>
        </button>
        <picture-options
          v-if="pictureOptionsOpen"
          :initial-title="currentSelection"
          @add="handleAddPicture"
          @close="
            pictureOptionsOpen = false
            focus()
          "
        />
        <button
          tabindex="-1"
          @click="handlePicture"
          title="Picture"
          class="btn-mdctrl"
        >
          <i class="fas fa-image"></i>
        </button>
        <button
          tabindex="-1"
          @click="handleCode"
          title="Code Block"
          class="btn-mdctrl"
        >
          <i class="fas fa-code"></i>
        </button>
      </div>
    </div>
    <div class="markdown-editor_input">
      <textarea
        @focus="resetModals"
        ref="input"
        class="form-control"
        :class="{ 'is-invalid': error }"
        :value="value"
        :style="{ height: height + 'px' }"
        @keydown="handleKeydown"
        @keyup="handleSelectionChange"
        @mouseup="handleSelectionChange"
        @input="handleInput"
      />
    </div>
    <slot></slot>
  </div>
</template>

<script lang="ts">
import LinkOptions from './LinkOptions.vue'
import PictureOptions from './PictureOptions.vue'
import UsernamePicker from './UsernamePicker.vue'

const isCtrlEnter = (e: KeyboardEvent) => {
  if (e.keyCode !== 13) {
    return false
  }

  if (window.navigator.platform.startsWith('Mac')) {
    return e.metaKey
  } else {
    return e.ctrlKey
  }
}

import { Vue, Component, Prop } from 'vue-property-decorator'

@Component({
  components: {
    LinkOptions,
    PictureOptions,
    UsernamePicker
  }
})
export default class MarkdownEditor extends Vue {
  @Prop({ type: String, required: true }) value!: string
  @Prop({ type: Number, default: 300 }) height!: number
  @Prop({ type: Boolean, default: true }) autofocus!: boolean
  @Prop({ type: Boolean, default: false }) error!: boolean

  private linkOptionsOpen = false
  private pictureOptionsOpen = false
  private usernamePickerOpen = false
  private currentSelection = ''

  get input() {
    return this.$refs.input as HTMLTextAreaElement
  }

  handleInput(e: InputEvent) {
    let { value } = this.input
    if (
      e.inputType === 'insertLineBreak' ||
      (e.inputType === 'insertText' && e.data === null)
    ) {
      const possiblePrefixes = ['> ', '1. ', '  * ']
      const { selectionEnd } = this.input
      const prev = this.previousLine(value, selectionEnd - 1)
      for (let i = 0; i < possiblePrefixes.length; i++) {
        const ins = possiblePrefixes[i]
        if (prev.startsWith(ins)) {
          value = value.slice(0, selectionEnd) + ins + value.slice(selectionEnd)
          this.$emit('input', value)
          const newEnd = selectionEnd + ins.length
          this.setSelectionAndFocus(newEnd)
          return
        }
      }
    }
  }

  handleKeydown(e: KeyboardEvent) {
    if (isCtrlEnter(e)) {
      this.$emit('submit')
    }
  }

  insert(ins: string) {
    const { selectionStart, selectionEnd } = this.input
    const newValue =
      this.value.slice(0, selectionStart) + ins + this.value.slice(selectionEnd)
    this.$emit('input', newValue)
    this.setSelectionAndFocus(selectionStart + ins.length)
  }

  previousLine(value: string, pos: number) {
    let end = pos
    while (end >= 0) {
      if (value[end] === '\n') break
      end--
    }
    if (end < 0) return ''
    let start = end - 1
    while (start >= 0) {
      if (value[start] === '\n') break
      start--
    }
    return value.slice(start + 1, end + 1)
  }

  isNewLine() {
    const { selectionStart } = this.input
    return this.value[selectionStart - 1] === '\n'
  }

  handleSelectionChange() {
    const { selectionStart, selectionEnd } = this.input
    this.currentSelection = this.value.slice(selectionStart, selectionEnd)
  }

  resetModals() {
    this.linkOptionsOpen = false
    this.usernamePickerOpen = false
    this.pictureOptionsOpen = false
  }

  selectedLinesBounds() {
    let start = this.input.selectionStart
    let end = this.input.selectionEnd
    // searching for the previous line end or the begining of the value
    while (start > 0) {
      if (start > 1 && this.value[start - 1] === '\n') {
        break
      }
      start--
    }

    // searching for the current line end or the end of the value
    while (end < this.value.length && this.value[end - 1] !== '\n') {
      end++
    }
    return { start, end }
  }

  prefixLines(prefix: string) {
    const { start, end } = this.selectedLinesBounds()
    let value = this.value.slice(start, end)
    let lines = []
    while (value.length) {
      const i = value.indexOf('\n')
      if (i < 0) {
        lines.push(value)
        break
      } else {
        lines.push(value.slice(0, i + 1))
        value = value.slice(i + 1)
      }
    }
    if (!lines.length) {
      lines = ['']
    }

    const removePrefix = lines[0].startsWith(prefix)
    const replace = lines
      .map(line => {
        if (removePrefix) {
          if (line.startsWith(prefix)) {
            return line.slice(prefix.length)
          }
          return line
        } else {
          if (!line.startsWith(prefix)) {
            return prefix + line.trimLeft()
          }
          return line
        }
      })
      .join('')

    const newValue =
      this.value.slice(0, start) + replace + this.value.slice(end)
    this.$emit('input', newValue)
    const newEnd = start + replace.length
    const newStart = start === end ? start + replace.length : start
    this.setSelectionAndFocus(newStart, newEnd)
  }

  setSelectionAndFocus(start: number, end?: number) {
    this.$nextTick(() => {
      if (typeof end === 'undefined') {
        end = start
      }
      this.input.selectionStart = start
      this.input.selectionEnd = end
      this.input.focus()
    })
  }

  wrapSelection(wrapper: string) {
    let { selectionStart, selectionEnd } = this.input
    const wrapperLength = wrapper.length

    const unwrap =
      selectionStart >= wrapperLength &&
      this.value.slice(selectionStart - wrapperLength, selectionStart) ===
        wrapper &&
      selectionEnd + wrapperLength <= this.value.length &&
      this.value.slice(selectionEnd, selectionEnd + wrapperLength) === wrapper

    let newValue
    const selection = this.value.slice(selectionStart, selectionEnd)

    if (unwrap) {
      newValue =
        this.value.slice(0, selectionStart - wrapperLength) +
        selection +
        this.value.slice(selectionEnd + wrapperLength)
      selectionStart = selectionStart - wrapperLength
      selectionEnd = selectionEnd - wrapperLength
    } else {
      newValue =
        this.value.slice(0, selectionStart) +
        wrapper +
        selection +
        wrapper +
        this.value.slice(selectionEnd)
      selectionStart = selectionStart + wrapperLength
      selectionEnd = selectionEnd + wrapperLength
    }
    this.$emit('input', newValue)
    this.setSelectionAndFocus(selectionStart, selectionEnd)
  }

  handleCode() {
    const { start, end } = this.selectedLinesBounds()

    let replace = this.value.slice(start, end)
    if (replace.split('\n').length > 1) {
      if (replace.startsWith('```\n') && replace.endsWith('```\n')) {
        replace = replace.slice(4, replace.length - 4)
      } else {
        if (end >= this.value.length && !this.value.endsWith('\n')) {
          // force add a newline
          replace = replace + '\n'
        }
        replace = '```\n' + replace + '```\n'
      }
      this.$emit(
        'input',
        this.value.slice(0, start) + replace + this.value.slice(end)
      )
      this.setSelectionAndFocus(start, start + replace.length)
    } else {
      this.wrapSelection('`')
    }
  }

  handleHeader() {
    this.prefixLines('## ')
  }
  handleUnorderedList() {
    this.prefixLines('  * ')
  }
  handleOrderedList() {
    this.prefixLines('1. ')
  }
  handleQuote() {
    this.prefixLines('> ')
  }
  handleBold() {
    this.wrapSelection('**')
  }
  handleItalic() {
    this.wrapSelection('_')
  }
  handleStrike() {
    this.wrapSelection('~~')
  }
  handleLink() {
    this.pictureOptionsOpen = false
    this.usernamePickerOpen = false
    this.linkOptionsOpen = !this.linkOptionsOpen
  }
  handlePicture() {
    this.usernamePickerOpen = false
    this.linkOptionsOpen = false
    this.pictureOptionsOpen = !this.pictureOptionsOpen
  }
  handleUsername() {
    this.linkOptionsOpen = false
    this.pictureOptionsOpen = false
    this.usernamePickerOpen = !this.usernamePickerOpen
  }
  handleAddLink(linkOptions: { title: string; link: string }) {
    let { title } = linkOptions
    const { link } = linkOptions
    if (title === '') {
      title = link
    }
    const linkRender = `[${title}](${link})`
    this.insert(linkRender)
  }
  handleAddUsername(username: string) {
    if (username !== '') {
      this.insert(`@${username}`)
    }
    this.usernamePickerOpen = false
  }
  handleAddPicture(picOptions: { title: string; link: string; width: string }) {
    const { title, link, width } = picOptions
    if (link !== '') {
      let value = `![${title}](${link}`
      if (width) {
        value += ` =${width}x${width}`
      }
      value += ')'
      this.insert(value)
    }
    this.pictureOptionsOpen = false
  }
  focus() {
    this.input.focus()
  }
}
</script>

<style lang="scss">
.markdown-editor {
  padding: 8px;
  background: white;
  border: 1px solid #999999;
  display: flex;
  flex-wrap: wrap;
  .markdown-editor_control_buttons {
    width: 100%;
  }
  .markdown-editor_input {
    flex-grow: 1;
  }
}

.markdown-editor .btn-group .btn {
  padding-left: 14px;
  padding-right: 14px;
}

.markdown-editor_control_buttons {
  .btn-group {
    margin-right: 8px;
    margin-bottom: 8px;
  }
}

.markdown-editor_input {
  margin-top: 4px;
}

.markdown-editor_input textarea {
  height: 300px;
  font-family: 'PT Mono';
  font-size: 14px;
}

.markdown-editor_disclaimer {
  text-align: right;
  color: #444444;
  font-weight: 300;
  font-family: 'Open Sans';
  font-style: italic;
}

.editor_link_options,
.picture_options,
.username_picker {
  border: 1px solid #eeeeee;
  text-align: left;
  z-index: 100;
  width: 280px;
  padding: 20px;
  top: 34px;
}

.editor_link_options {
  left: 30px;
}

.username_picker {
  left: 150px;
  .suggest-list {
    position: absolute;
    width: 350px;
  }
}

.picture_options {
  left: 206px;
  width: 320px;
}

.picture_options-img_preview {
  position: relative;
  width: 200px;
  height: 200px;
  background-color: #eee;
  margin: 12px auto;
  border: 1px solid gray;
  display: flex;
  justify-content: space-around;
  align-items: center;
  flex-direction: column;
  overflow: hidden;
  img {
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    z-index: 3;
  }
}
.picture_options-img_preview::after {
  position: absolute;
  display: block;
  content: 'Preview';
  width: 100%;
  top: calc(50% - 0.75em);
  text-align: center;
  color: gray;
  z-index: 0;
}

.suggest-list {
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 0.9rem;
  max-height: 52px * 5;
  overflow: auto;
}

.suggest-list-item {
  padding: 4px 12px;
  cursor: pointer;
  height: 52px;
}

.suggest-list-item.active {
  background-color: var(--primary);
  color: white;
}

.shadow-block {
  box-shadow: 0 5px 8px 0 rgba(0, 0, 0, 0.25);
  background-color: white;
}

.floating-block {
  position: absolute;
  z-index: 300;
}

.btn-mdctrl {
  border: none;
  background-color: white;
  width: 38px;
  height: 38px;
  font-size: 0.9em;
  transition: background-color 0.15s linear;
  &:hover {
    background-color: #eeeeee;
  }
}
</style>
