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
        placeholder="Ссылка"
        v-model="link"
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
        placeholder="Alt (опционально)"
        v-model="title"
      />
    </div>
    <div class="form-group">
      <input
        class="form-control form-control-sm"
        type="text"
        placeholder="Ширина (опционально)"
        v-model="width"
      />
    </div>
    <div>
      <button @click="handleSave" class="btn btn-sm btn-primary"
        >Добавить</button
      >
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
      title: '',
      width: ''
    }
  },
  mounted() {
    this.title = this.initialTitle
    this.$refs.linkInput.focus()
  },
  methods: {
    handleSave() {
      const { link, title } = this
      let width = parseInt(this.width)
      if (isNaN(width)) width = null
      this.$emit('add', { link, title, width })
    }
  }
}
</script>
