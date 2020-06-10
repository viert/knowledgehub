<template>
  <div class="post-markdown">
    <component :is="compiledBody" />
  </div>
</template>

<script>
import Vue from 'vue'
import MarkDown from '@/markdown'

export default {
  props: {
    body: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      compiledBody: null
    }
  },
  methods: {
    recompile() {
      const html = MarkDown.makeHtml(this.body)
        .replace(/{/g, '<span>&lbrace;</span>')
        .replace(/}/g, '<span>&rbrace;</span>')
      this.compiledBody = Vue.compile(`<fragment>${html}</fragment>`)
    }
  },
  mounted() {
    this.recompile()
  },
  watch: {
    body() {
      this.recompile()
    }
  }
}
</script>

<style lang="scss"></style>
