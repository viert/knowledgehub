<template>
  <div class="post-markdown" :class="{ 'post-markdown--inline': inline }">
    <component :is="compiledBody" />
  </div>
</template>

<script lang="ts">
import { VNode } from 'vue'
import { Vue, Component, Prop, Watch } from 'vue-property-decorator'
import MarkDown, { plainConverter } from '@/markdown'

@Component
export default class Post extends Vue {
  @Prop({ type: String, required: true }) readonly body!: string
  @Prop({ type: Boolean, default: false }) readonly strict!: boolean
  @Prop({ type: Boolean, default: false }) readonly inline!: boolean

  private compiledBody: {
    render(createElement: any): VNode
    staticRenderFns: (() => VNode)[]
  } | null = null

  recompile() {
    let html: string
    if (this.strict) html = plainConverter(this.body)
    else {
      html = MarkDown.makeHtml(this.body)
        .replace(/{/g, '<span>&lbrace;</span>')
        .replace(/}/g, '<span>&rbrace;</span>')
    }
    this.compiledBody = Vue.compile(`<fragment>${html}</fragment>`)
  }

  mounted() {
    this.recompile()
  }

  @Watch('body')
  onBodyChange() {
    this.recompile()
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
