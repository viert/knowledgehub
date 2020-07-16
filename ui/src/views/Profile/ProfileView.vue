<template>
  <div class="page-layout">
    <main>
      <h3 class="page-title">Profile</h3>
      <div v-if="!ready" class="loading loading--user-settings">
        <Progress text="loading" />
      </div>
      <fragment v-else>
        <div class="user-settings">
          <div class="user-settings_avatar">
            <img :src="user.avatar_url" />
          </div>
          <form class="user-settings_form">
            <FormRow label="Your ID" v-model="user.ext_id" :readonly="true" />
            <FormRow label="Username" v-model="user.username" />
            <FormRow label="First Name" v-model="user.first_name" />
            <FormRow label="Last Name" v-model="user.last_name" />
            <hr />
            <FormRow label="Email" v-model="user.email" />
            <FormRow label="Telegram ID" v-model="user.telegram_id" />
            <FormRow label="ICQ ID" v-model="user.icq_id" />
            <p>
              To get Telegram and/or ICQ notifications, set your account ID here, then add %TODO_BOT_ACCOUNT% and run
              <code>/start</code> command.
            </p>
          </form>
        </div>
      </fragment>
    </main>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import FormRow from './FormRow'
import RequireAuth from '@/mixins/RequireAuth'

export default {
  mixins: [RequireAuth],
  components: {
    FormRow
  },
  data() {
    return {
      user: {}
    }
  },
  computed: {
    ...mapGetters({
      me: 'users/me'
    })
  },
  watch: {
    ready() {
      this.user = { ...this.me }
    }
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
