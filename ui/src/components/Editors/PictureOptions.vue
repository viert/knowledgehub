<template>
  <form
    @submit.prevent="handleSave"
    class="shadow-block floating-block picture_options"
  >
    <div class="form-group">
      <input
        ref="linkInput"
        class="form-control form-control-sm"
        type="text"
        placeholder="Link"
        v-model="link"
        @keydown.esc="$emit('close')"
      />
    </div>
    <div class="picture_options-img_preview">
      <img :src="link" :title="title" />
    </div>
    <div class="form-group">
      <input
        ref="titleInput"
        class="form-control form-control-sm"
        type="text"
        placeholder="Alt Text (optional)"
        v-model="title"
        @keydown.esc="$emit('close')"
      />
    </div>
    <div class="form-group">
      <input
        class="form-control form-control-sm"
        type="text"
        placeholder="Width (optional)"
        @keydown.esc="$emit('close')"
        v-model="width"
      />
    </div>
    <div>
      <button @click="handleSave" class="btn btn-sm btn-primary">Add</button>
    </div>
  </form>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component
export default class PictureOptions extends Vue {
  @Prop({ type: String, default: '' }) readonly initialTitle!: string

  private link = ''
  private title = ''
  private width = ''

  mounted() {
    this.title = this.initialTitle
    const input = this.$refs.linkInput as HTMLInputElement
    input.focus()
  }

  handleSave() {
    const { link, title } = this
    let width: number | null = parseInt(this.width)
    if (isNaN(width)) width = null
    this.$emit('add', { link, title, width })
  }
}
</script>
