<template>
  <li ref="root" class="comment">
    <fragment v-if="!isEditing">
      <div class="comment-voter">
        <Voter
          :mini="true"
          @input="handleVote"
          :points="comment.points"
          :value="comment.my_vote"
        />
      </div>
      <div
        class="comment-body"
        :class="{ flash: comment.flash, deleted: this.comment.deleted }"
      >
        <Post :body="comment.body" :strict="true" :inline="true" />&mdash;
        <User :username="author.username" />
        {{ comment.created_at | duration }}
        <div v-if="isMyComment">
          <PostActions
            @edit="handleEdit"
            @delete="handleDelete"
            @restore="handleRestore"
            :isSaving="isSaving"
            :isDeleted="this.comment.deleted"
          />
        </div>
      </div>
    </fragment>
    <div v-else class="comment-edit">
      <textarea
        v-model="body"
        class="form-control"
        ref="commentEditor"
        :class="{ 'is-invalid': error }"/>
      <div v-if="error" class="error-msg">{{ error }}</div>
      <PostEditorActions
        name="comment"
        @cancel="handleCancel"
        :isSaving="isSaving"
        @save="handleSave"
    /></div>
  </li>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import Post from '@/components/Post.vue'
import PostActions from '@/components/PostActions.vue'
import PostCommons from '@/mixins/PostCommons'
import { Comment, User } from '@/store/types'
import { mixins } from 'vue-class-component'
import PostEditorActions from '@/components/PostEditorActions.vue'
import { namespace } from 'vuex-class'
const users = namespace('users')

@Component({ components: { PostEditorActions, Post, PostActions } })
export default class CommentView extends mixins(PostCommons) {
  @users.Getter('me') readonly me!: User
  @Prop({ type: Object, required: true }) readonly comment!: Comment
  private isSaving = false
  private isEditing = false
  private body = this.comment.body
  private error: string | null = null

  handleVote(value: 1 | 0) {
    this.$store.dispatch('questions/voteComment', {
      commentId: this.comment._id,
      value
    })
  }

  get commentEditor() {
    return this.$refs.commentEditor
  }

  get author() {
    return this.getUser(this.comment.author_id)
  }

  handleDelete() {
    this.$store.dispatch('questions/deleteComment', this.comment._id)
  }

  handleRestore() {
    this.$store.dispatch('questions/restoreComment', this.comment._id)
  }

  get isMyComment() {
    return Boolean(this.me && this.me._id === this.comment.author_id)
  }
  handleSave() {
    if (this.body.trim() === '') {
      this.error = "Comment can't be empty"
      this.commentEditor.focus()
      return
    }

    this.isSaving = true

    this.$store
      .dispatch('questions/editComment', {
        commentId: this.comment._id,
        body: this.body,
        parentId: this.comment.parent_id // answerId, if exists
      })
      .finally(() => {
        this.isSaving = false
        this.isEditing = false
      })
  }

  handleEdit() {
    this.isEditing = true

    if (this.error) {
      this.error = null
    }
  }

  handleCancel() {
    this.isEditing = false
  }
}
</script>

<style lang="scss">
li.comment {
  display: flex;
  border-top: 1px solid #cccccc;
  padding: 8px 0;

  .comment-voter {
    min-width: 32px;
  }

  .comment-body {
    flex-grow: 1;
    font-size: 0.9em;
  }

  .comment-edit {
    width: 100%;
  }

  .deleted {
    opacity: 0.4;
  }
}
</style>
