<template>
  <div class="page-header">
    <div class="logo">
      <router-link to="/">
        knowledge
        <span style="color: #fc2c38;">hub</span>
      </router-link>
    </div>
    <div class="panel">
      <div class="panel-search">
        <input type="text" class="form-control searchbox" />
      </div>
      <div class="panel-account">
        <a href>Sign in</a>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState({
      me: state => state.user.user
    }),
    avatarURL() {
      if (this.me.avatar) {
        return this.me.avatar
      }
      return '/images/default_user.png'
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('user/logout')
    }
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
    }
  }
}
</style>
