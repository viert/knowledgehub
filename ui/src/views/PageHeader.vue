<template>
  <div class="page-header">
    <div class="logo">
      <!--prettyhtml-ignore-->
      <router-link to="/">
        knowledge<span style="color: #fc2c38;">hub</span>
      </router-link>
    </div>
    <div class="panel">
      <div class="panel-search">
        <input type="text" class="form-control searchbox" />
      </div>
      <div v-if="me" class="panel-account">
        <User :username="me.username" />
        <a class="logout" href="" @click.prevent="logout">
          <i class="fas fa-sign-out-alt"></i>
        </a>
      </div>
      <div v-else-if="authInfoAcquired" class="panel-account">
        <router-link to="/signin">
          Sign in
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import User from '@/components/User'
import { mapGetters, mapState, mapActions } from 'vuex'
import { AuthStates } from '@/constants'

export default {
  components: {
    User
  },
  computed: {
    ...mapGetters({
      me: 'users/me'
    }),
    ...mapState({
      authState: 'users/authState'
    }),
    authInfoAcquired() {
      return this.authState !== AuthStates.Unknown
    },
    avatarURL() {
      if (this.me.avatar) {
        return this.me.avatar
      }
      return '/images/default_user.png'
    }
  },
  methods: {
    ...mapActions({ logout: 'users/logout' })
  }
}
</script>

<style lang="scss">
$avatar-size: 40px;

.logo {
  font-family: Questrial;
  font-size: 28px;
  font-weight: normal;
}

.page-header {
  height: 56px;
  display: flex;
  align-items: center;
  background-color: white;
  border-bottom: 1px solid #dfd7ca;
  .logo {
    display: flex;
    height: 26px;
    margin-left: 36px;
    a {
      color: black;
      height: 26px;
      line-height: 26px;
      text-decoration: none !important;
    }
  }

  .panel {
    flex-grow: 1;
    display: flex;
    margin-left: 10px;

    height: 56px;

    .panel-search {
      display: flex;
      flex-grow: 1;
      justify-content: flex-end;
      align-items: center;
      position: relative;

      &:before {
        display: block;
        font-family: 'Font Awesome 5 Free';
        font-weight: bold;
        content: '\f002';
      }

      input.searchbox {
        width: 280px;
        margin-left: 12px;
      }
    }

    .panel-account {
      display: flex;
      align-items: center;
      padding: 0 20px;
      a {
        color: black;
        font-weight: bold;
      }
      a.logout {
        margin-left: 8px;
        color: gray;
        &:hover {
          color: black;
        }
      }
    }
  }
}
</style>
