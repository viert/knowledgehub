<template>
  <form
    @submit.prevent="handleSave"
    class="shadow-block floating-block editor_link_options"
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
    <div class="form-group">
      <input
        ref="titleInput"
        class="form-control form-control-sm"
        type="text"
        placeholder="Title"
        v-model="title"
        @keydown.esc="$emit('close')"
      />
    </div>
    <div>
      <button @click="handleSave" class="btn btn-sm btn-primary">Add</button>
    </div>
  </form>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit } from 'vue-property-decorator'

@Component
export default class LinkOptions extends Vue {
  @Prop({ type: String, default: '' }) readonly initialTitle!: string

  private link = ''
  private title = ''

  mounted() {
    this.title = this.initialTitle
    const input = this.$refs.linkInput as HTMLInputElement
    input.focus()
  }

  @Emit('add')
  handleSave() {
    return { link: this.link, title: this.title }
  }
}
</script>
