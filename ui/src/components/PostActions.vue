<template>
  <div class="post-actions">
    <a @click.prevent="handleEdit" href="#">
      <i class="fas fa-edit"></i> edit
    </a>
    <a v-if="!isDeleted" @click.prevent="handleDelete" href="#">
      <i class="fas fa-trash"></i> delete
    </a>
    <a v-else @click.prevent="handleRestore" href="#">
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
  a {
    font-size: 14px;
    color: black;
    text-decoration: none;
    &:hover {
      color: #426d98;
    }
    i.fas,
    i.far {
      font-size: 0.75em;
    }
    margin-right: 0.5em;
  }
}
</style>
