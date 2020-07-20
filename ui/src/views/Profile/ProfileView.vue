<template>
  <div class="page-layout">
    <main>
      <h3 class="page-title">Profile</h3>
      <div v-if="loading" class="loading loading--user-settings">
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
              :disabled="saving"
              :readonly="true"
            />
            <FormRow
              label="Username"
              v-model="user.username"
              :disabled="saving"
            />
            <FormRow
              label="First Name"
              v-model="user.first_name"
              :disabled="saving"
            />
            <FormRow
              label="Last Name"
              v-model="user.last_name"
              :disabled="saving"
            />
            <hr />
            <FormRow label="Email" v-model="user.email" :disabled="saving" />
            <FormRow
              label="Telegram ID"
              v-model="user.telegram_id"
              :disabled="saving"
            />
            <FormRow label="ICQ ID" v-model="user.icq_id" :disabled="saving" />
            <FormRow label="Notifications">
              <ButtonSwitch v-model="notificationOptions" :disabled="saving" />
            </FormRow>
            <p>
              To get Telegram and/or ICQ notifications, set your account ID
              here, then add %TODO_BOT_ACCOUNT% and run
              <code>/start</code> command.
            </p>
            <div class="post-form-control">
              <SpinnerButton
                type="submit"
                :loading="saving"
                class="btn btn-primary"
                >Save Settings</SpinnerButton
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
import { namespace } from 'vuex-class'
import { mixins } from 'vue-class-component'
import { User } from '@/store/types'

const users = namespace('users')

@Component({ components: { FormRow } })
export default class ProfileView extends mixins(RequireAuth) {
  private user: User | null = null
  private notificationOptions = { email: true, telegram: false, icq: false }
  private loading = false
  private saving = false

  @users.Getter('me') me!: User

  handleSave() {
    const settings = {
      ...this.user,
      notify_by_email: this.notificationOptions.email,
      notify_by_icq: this.notificationOptions.icq,
      notify_by_telegram: this.notificationOptions.telegram
    }
    this.saving = true
    this.$store
      .dispatch('users/saveSettings', settings)
      .then(() => {
        this.fillUser()
        this.$store.dispatch('messages/info', 'Settings saved successfully')
      })
      .finally(() => {
        this.saving = false
      })
  }

  fillUser() {
    this.user = { ...this.me }
    this.notificationOptions = {
      email: this.me.notify_by_email,
      telegram: this.me.notify_by_telegram,
      icq: this.me.notify_by_icq
    }
    this.loading = false
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

.user-settings {
  padding: 2em;
  box-sizing: border-box;
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
    flex-grow: 1;
  }

  label {
    font-family: Montserrat;
    text-transform: uppercase;
  }
}
</style>
