<template>
  <div ref="root" class="question">
    <fragment v-if="!isEditing">
      <h2>{{ question.title }}</h2>
      <hr />

      <div class="question-post">
        <div class="question-vote">
          <Voter
            @input="handleVote"
            :points="question.points"
            :value="question.my_vote"
          />
        </div>
        <div
          :class="{
            'question-body': true,
            'question-body__deleted': question.deleted
          }"
        >
          <Post :body="question.body" />
          <div class="question-meta">
            <div class="question-meta__wrapper">
              <div class="question-tags">
                <Tag v-for="tag in question.tags" :key="tag" :name="tag" />
              </div>
              <div class="question-actions" v-if="isMyQuestion">
                <PostActions
                  @edit="openEditor"
                  @delete="handleDelete"
                  @restore="handleRestore"
                  :isDeleted="isDeleted"
                />
              </div>
            </div>
            <div class="question-author">
              <AuthorCard
                action="Asked"
                :author="author"
                :askedAt="question.created_at"
              />
            </div>
          </div>

          <CommentsList :parentId="question._id" :comments="selfComments" />
        </div>
      </div>
    </fragment>
    <fragment v-else
      ><QuestionEdit
        :question="question"
        :isSaving="isSaving"
        @save="onSave"
        @cancel="onCancel"
    /></fragment>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import PostCommons from '@/mixins/PostCommons'
import { mixins } from 'vue-class-component'
import Post from '@/components/Post.vue'
import PostActions from '@/components/PostActions.vue'
import CommentsList from './CommentsList.vue'
import AuthorCard from './AuthorCard.vue'
import QuestionEdit from '@/views/Questions/Partial/QuestionEdit.vue'
import { Question, Comment, User } from '@/store/types'
import { namespace } from 'vuex-class'
const users = namespace('users')

@Component({
  components: { Post, CommentsList, AuthorCard, PostActions, QuestionEdit }
})
export default class QuestionView extends mixins(PostCommons) {
  @users.Getter('me') readonly me!: User
  @Prop({ type: Object, required: true }) question!: Question
  @Prop({ type: Array, default: () => [] }) readonly comments!: Comment[]
  private isEditing = false
  private isSaving = false

  handleVote(value: 1 | 0 | -1) {
    this.$store.dispatch('questions/voteQuestion', value)
  }

  get selfComments() {
    return this.comments.filter(c => c.parent_id === this.question._id)
  }

  handleDelete() {
    this.$store.dispatch('questions/deleteQuestion')
  }

  handleRestore() {
    this.$store.dispatch('questions/restoreQuestion')
  }

  openEditor() {
    this.isEditing = true
  }

  get isDeleted() {
    return this.question.deleted
  }

  get author() {
    return this.getUser(this.question.author_id)
  }

  onSave(data: object) {
    this.isSaving = true
    this.$store.dispatch('questions/editQuestion', data).finally(() => {
      this.isSaving = false
      this.isEditing = false
    })
  }

  onCancel() {
    this.isEditing = false
  }
}
</script>

<style lang="scss">
.question,
.answer {
  h2 {
    font-weight: bold;
  }

  &-post {
    display: flex;
  }
  &-vote {
    min-width: 60px;
    width: 60px;
    margin-right: 12px;
  }
  &-body {
    flex-grow: 1;
  }

  &-body__deleted {
    opacity: 0.5;
  }

  &-meta {
    display: flex;
    justify-content: flex-end;
  }

  &-meta__wrapper {
    flex-grow: 1;
  }

  &-tags {
    flex-grow: 1;
  }

  .question-actions {
    margin: 10px 0;
  }
}
</style>
