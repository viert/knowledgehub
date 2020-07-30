<template>
  <div class="answer-edit-actions">
    <button class="btn btn-secondary cancel" @click="cancel">Cancel</button>

    <SpinnerButton
      @click="save"
      class="btn btn-primary btn-150 "
      type="submit"
      :loading="isSaving"
      >Save {{ name }}</SpinnerButton
    >
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import PostCommons from '@/mixins/PostCommons'
import Post from '@/components/Post.vue'
import PostActions from '@/components/PostActions.vue'
import Accept from '@/components/Accept.vue'
import CommentsList from '../views/Questions/Partial/CommentsList.vue'
import AuthorCard from '../views/Questions/Partial/AuthorCard.vue'
import MarkdownEditor from '@/components/Editors/MarkdownEditor.vue'
import { mixins } from 'vue-class-component'

@Component({
  components: {
    Post,
    CommentsList,
    AuthorCard,
    Accept,
    PostActions,
    MarkdownEditor
  }
})
export default class PostEditorActions extends mixins(PostCommons) {
  @Prop({ type: Boolean, required: true }) readonly isSaving!: boolean
  @Prop({ type: String, required: true }) readonly name!: boolean

  save() {
    this.$emit('save')
  }

  cancel() {
    this.$emit('cancel')
  }
}
</script>

<style lang="scss">
.answer-edit-actions {
  margin: 10px 0;
  display: flex;
  justify-content: flex-end;
}

.cancel {
  margin-right: 10px;
}
</style>
