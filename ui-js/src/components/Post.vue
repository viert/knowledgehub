<template>
  <div class="post-markdown" :class="{'post-markdown--inline': inline}">
    <component :is="compiledBody" />
  </div>
</template>

<script>
import Vue from 'vue'
import MarkDown, { plainConverter } from '@/markdown'

export default {
  props: {
    body: {
      type: String,
      required: true
    },
    strict: {
      type: Boolean,
      default: false
    },
    inline: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      compiledBody: null
    }
  },
  methods: {
    recompile() {
      let html
      if (this.strict) html = plainConverter(this.body)
      else {
        html = MarkDown.makeHtml(this.body)
          .replace(/{/g, '<span>&lbrace;</span>')
          .replace(/}/g, '<span>&rbrace;</span>')
      }
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

<style lang="scss">
.post-markdown {
  strong {
    font-weight: bold;
  }

  blockquote {
    margin: 0 0 1em 1.5em;
    padding: 4px 4px 4px 0.5em;
    background: #eeeeee;
    border-left: 3px solid #999999;
    p {
      margin: 0;
    }
  }

  &.post-markdown--inline {
    display: inline;
  }
}
</style>
