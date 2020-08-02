<template>
  <div class="page-layout">
    <main>
      <h3 class="page-title">Profile</h3>
      <div v-if="isLoading" class="loading loading--user-settings">
        <Progress text="loading" />
      </div>
      <fragment v-else>
        <div class="user-settings">
          <div class="user-settings_avatar">
            <img :src="user.avatar_url" />
          </div>
          <form @submit.prevent="handleSave" class="user-settings_form">
            <FormRow
              label="Your ID"
              v-model="user.ext_id"
              :disabled="isSaving"
              :readonly="true"
            />
            <FormRow
              label="Username"
              v-model="user.username"
              :disabled="isSaving"
            />
            <FormRow
              label="First Name"
              v-model="user.first_name"
              :disabled="isSaving"
            />
            <FormRow
              label="Last Name"
              v-model="user.last_name"
              :disabled="isSaving"
            />
            <hr />
            <FormRow
              v-if="bots.telegram"
              label="Telegram ID"
              v-model="user.telegram_id"
              :disabled="isSaving"
            >
              <template v-slot:info>
                To get telegram notifications, set your ID here, then add
                <a target="_blank" :href="bots.telegram.link"
                  >@{{ bots.telegram.name }}</a
                >
                to your contact list and type <code>/start</code>
              </template>
            </FormRow>
            <FormRow
              v-if="bots.icq"
              label="ICQ ID"
              v-model="user.icq_id"
              :disabled="isSaving"
            >
              <template v-slot:info>
                To get ICQ notifications, set your ID here, then add
                <a target="_blank" :href="bots.icq.link"
                  >@{{ bots.icq.name }}</a
                >
                to your contact list and type <code>/start</code>
              </template>
            </FormRow>
            <div class="post-form-control">
              <SpinnerButton
                type="submit"
                :loading="isSaving"
                class="btn btn-primary btn-150"
                >Save Settings</SpinnerButton
              >
            </div>
          </form>
        </div>
        <h3 class="page-title">Subscriptions</h3>
        <div class="tags-settings">
          <form @submit.prevent="handleSaveTags" class="tags-settings_form">
            <FormRow label="tags" :disabled="tagsAreSaving">
              <TagEditor
                :tags="tags"
                @add="handleAddTag"
                @remove="handleRemoveTag"
              />
            </FormRow>
            <div class="post-form-control">
              <SpinnerButton
                type="submit"
                :loading="tagsAreSaving"
                class="btn btn-primary btn-150"
                >Save Tags</SpinnerButton
              >
            </div>
          </form>
        </div>
      </fragment>
    </main>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import FormRow from './FormRow.vue'
import RequireAuth from '@/mixins/RequireAuth'
import TagEditor from '@/components/Editors/TagEditor.vue'
import { namespace } from 'vuex-class'
import { mixins } from 'vue-class-component'
import { User, BotDescription } from '@/store/types'

const users = namespace('users')
const events = namespace('events')

@Component({ components: { FormRow, TagEditor } })
export default class ProfileView extends mixins(RequireAuth) {
  private user: User | null = null
  private tags: string[] | null = null
  private isLoading = true
  private isSaving = false
  private tagsAreSaving = false

  @users.Getter('me') readonly me!: User
  @users.State('tagSubscriptions') readonly tagSubscriptions!: string[]
  @events.State('bots') readonly bots!: {
    icq?: BotDescription
    telegram?: BotDescription
  }

  handleSave() {
    this.isSaving = true
    this.$store
      .dispatch('users/saveSettings', this.user)
      .then(() => {
        this.fillUser()
        this.$store.dispatch('messages/info', 'Settings saved successfully')
      })
      .finally(() => {
        this.isSaving = false
      })
  }

  fillUser() {
    this.user = {
      ...this.me
    }
    this.tags = [...this.tagSubscriptions]
    this.isLoading = false
  }

  handleAddTag(tag: string) {
    if (this.tags) this.tags = [...this.tags, tag]
  }

  handleRemoveTag(tag: string) {
    if (this.tags) this.tags = this.tags.filter(t => t !== tag)
  }

  handleSaveTags() {
    if (this.user) {
      this.tagsAreSaving = true
      this.$store
        .dispatch('users/replaceTagSubscription', this.tags)
        .then(() => {
          this.fillUser()
          this.$store.dispatch('messages/info', 'Tags subscription updated')
        })
        .finally(() => {
          this.tagsAreSaving = false
        })
    }
  }

  onReady() {
    this.fillUser()
  }
}
</script>

<style lang="scss">
.loading--user-settings {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: calc(100vh - 220px);
}

.user-settings,
.tags-settings {
  padding: 2em;
  box-sizing: border-box;
  label {
    font-family: Montserrat;
    text-transform: uppercase;
  }
}

.user-settings {
  display: flex;

  .user-settings_avatar {
    width: 150px;
    min-width: 150px;
    height: 150px;
    overflow: hidden;
    border-radius: 50%;

    margin-right: 3em;
    img {
      width: 150px;
      height: 150px;
    }
  }
  .user-settings_form {
    width: 100%;
  }
}

.tags-settings {
  .tags-settings_form {
    margin-left: calc(3em + 150px);
  }
}
</style>
