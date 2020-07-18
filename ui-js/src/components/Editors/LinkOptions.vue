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

<script>
export default {
  props: {
    initialTitle: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      link: '',
      title: ''
    }
  },
  mounted() {
    this.title = this.initialTitle
    this.$refs.linkInput.focus()
  },
  methods: {
    handleSave() {
      const { link, title } = this
      this.$emit('add', { link, title })
    }
  }
}
</script>
