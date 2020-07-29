<template>
  <div ref="root" class="answer">
    <div class="answer-post">
      <div class="answer-vote">
        <Voter
          @input="handleVote"
          :points="answer.points"
          :value="answer.my_vote"
        />
        <Accept
          :readonly="!isMyQuestion"
          :value="answer.accepted"
          @input="handleAccept"
        />
      </div>
      <div
        :class="{ 'answer-body': true, deleted: answer.deleted }"
        v-if="!isEditView"
      >
        <Post :body="answer.body" />

        <div class="answer-meta">
          <div class="answer-actions">
            <PostActions
              v-if="isMyAnswer"
              :parentId="answer._id"
              :answer="answer"
              @delete="handleDelete"
              @restore="handleRestore"
              @edit="handleOpenEditor"
              :isDeleted="isDeleted"
            />
          </div>
          <div class="answer-author">
            <AuthorCard
              action="Answered"
              :author="author"
              :askedAt="answer.created_at"
            />
          </div>
        </div>
        <ul class="comments-section">
          <CommentsList :parentId="answer._id" :comments="selfComments" />
        </ul>
      </div>

      <AnswerEdit
        v-else
        ref="editor"
        :value="body"
        @save="handleSaveEdits"
        @cancel="handleCancelEdits"
        :isSaving="isSaving"
        :error="bodyError"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import PostCommons from '@/mixins/PostCommons'
import Post from '@/components/Post.vue'
import PostActions from '@/components/PostActions.vue'
import Accept from '@/components/Accept.vue'
import CommentsList from './CommentsList.vue'
import AuthorCard from './AuthorCard.vue'
import MarkdownEditor from '@/components/Editors/MarkdownEditor.vue'
import { Answer, Comment, User } from '@/store/types'
import { mixins } from 'vue-class-component'
import { namespace } from 'vuex-class'
import AnswerEdit from '@/views/Questions/Partial/AnswerEdit.vue'
const users = namespace('users')

@Component({
  components: {
    AnswerEdit,
    Post,
    CommentsList,
    AuthorCard,
    Accept,
    PostActions,
    MarkdownEditor
  }
})
export default class AnswerView extends mixins(PostCommons) {
  @Prop({ type: Object, required: true }) readonly answer!: Answer
  @Prop({ type: Array, default: () => [] }) readonly comments!: Comment[]
  @users.Getter('me') readonly me!: User

  private isEditView: boolean | false = false
  private isSaving: boolean | false = false
  private bodyError: string | null = null
  private body: string | '' = this.answer.body

  handleVote(value: 1 | 0 | -1) {
    this.$store.dispatch('questions/voteAnswer', {
      answerId: this.answer._id,
      value
    })
  }

  handleAccept() {
    if (this.answer.accepted) {
      this.$store.dispatch('questions/revokeAnswer', this.answer._id)
    } else {
      this.$store.dispatch('questions/acceptAnswer', this.answer._id)
    }
  }

  handleDelete(answerId: number) {
    this.$store.dispatch('questions/deleteAnswer', answerId)
  }

  handleRestore(answerId: number) {
    this.$store.dispatch('questions/restoreAnswer', answerId)
  }

  handleOpenEditor(answerId: number) {

    console.log('this.body ', this.body)
    this.isEditView = true

    if (this.bodyError ) {
      this.bodyError = null
    }
  }

  handleSaveEdits(body: object) {
    if (body.trim() === '') {
      this.bodyError = 'Body can not be empty'
      this.answerEditor.focus()
      return
    };


    this.isSaving = true
    const payload = {
      answerId: this.answer._id,
      body
    }
    this.$store
      .dispatch('questions/editAnswer', payload)
      .then(() => {
        this.isEditView = false
      })
      .finally(() => {
        this.isSaving = false
      })
  }

  handleCancelEdits() {
    this.isEditView = false
  }

  get selfComments() {
    return this.comments.filter(c => c.parent_id === this.answer._id)
  }

  get isDeleted() {
    return this.answer.deleted
  }

  get author() {
    return this.getUser(this.answer.author_id)
  }
  get isMyAnswer() {
    return Boolean(this.me && this.me._id === this.author._id)
  }

  get answerEditor() {
    return this.$refs.editor as AnswerEdit
  }
}
</script>

<style lang="scss">
.answer {
  border-top: 1px solid #cccccc;
  padding-top: 20px;
}
.deleted {
  opacity: 0.4;
}
.answer-actions {
  flex-grow: 1;
}
</style>
