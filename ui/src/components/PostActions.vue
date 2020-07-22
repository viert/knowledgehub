<template>
    <div class="post-"
</template>



<script lang="ts">
import { Vue, Component, Prop, Watch } from 'vue-property-decorator'
@Component
export default class PostActions extends Vue {
  @Prop({ type: String, required: true }) readonly body!: string
  @Prop({ type: Boolean, default: false }) readonly strict!: boolean
  @Prop({ type: Boolean, default: false }) readonly inline!: boolean


}
</script>
