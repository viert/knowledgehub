<template>
  <div class="post-actions">
    <a @click.prevent="handleEdit" href="#" class="icon-link">
      <i class="fas fa-edit"></i> edit
    </a>
    <a
      v-if="!isDeleted"
      @click.prevent="handleDelete"
      href="#"
      class="icon-link"
    >
      <i class="fas fa-trash"></i> delete
    </a>
    <a v-else @click.prevent="handleRestore" href="#" class="icon-link">
      <i class="fas fa-trash-restore"></i> restore
    </a>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component
export default class PostActions extends Vue {
  @Prop({ type: String, required: false }) readonly parentId!: string
  @Prop({ type: Boolean, required: true }) readonly isDeleted!: boolean

  handleDelete() {
    this.$emit('delete', this.parentId)
  }

  handleRestore() {
    this.$emit('restore', this.parentId)
  }

  handleEdit() {
    this.$emit('edit', this.parentId)
  }
}
</script>

<style lang="scss">
.post-actions {
  padding: 2px 0;
}
</style>
