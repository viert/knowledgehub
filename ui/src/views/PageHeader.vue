<template>
  <div class="page-header">
    <div class="logo">
      <!--prettyhtml-ignore-->
      <router-link to="/">
        knowledge<span style="color: #fc2c38;">hub</span>
      </router-link>
    </div>
    <div class="panel">
      <form @submit.prevent="handleSearch" class="panel-search">
        <input
          ref="search"
          type="text"
          v-model="searchQuery"
          class="form-control searchbox"
        />
      </form>
      <div class="panel-ask">
        <!--prettyhtml-ignore-->
        <router-link to="/ask" class="btn btn-primary btn-ask">
          Ask Question
        </router-link>
      </div>
      <div v-if="me" class="panel-account">
        <User
          :username="me.username"
          overrideLink="/profile"
          :moderator="me.moderator"
        />
        <a class="logout" href @click.prevent="logout">
          <i class="fas fa-sign-out-alt"></i>
        </a>
      </div>
      <div v-else-if="authInfoAcquired" class="panel-account">
        <router-link to="/signin">Sign in</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { User } from '@/store/types'
import { AuthState } from '@/constants'
import EventBus from '@/eventbus'
const users = namespace('users')

@Component
export default class PageHeader extends Vue {
  @users.Getter('me') readonly me!: User
  @users.State('authState') readonly authState!: AuthState
  @users.Action('logout') logout!: () => void

  private searchQuery = ''

  get authInfoAcquired() {
    return this.authState !== AuthState.Unknown
  }

  get avatarURL() {
    return this.me.avatar_url ? this.me.avatar_url : '/images/default_user.png'
  }

  onQueryChanged(query: string) {
    this.searchQuery = query
    this.$nextTick(() => {
      const search = this.$refs.search as HTMLInputElement
      search.focus()
    })
  }

  get q() {
    const q = this.$route.query.q
    if (typeof q === 'string') return q
    return ''
  }

  mounted() {
    if (this.$route.name === 'SearchResults') {
      this.onQueryChanged(this.q)
    }
    EventBus.$on('queryChanged', this.onQueryChanged)
  }

  beforeDestroy() {
    EventBus.$off('queryChanged', this.onQueryChanged)
  }

  handleSearch() {
    if (this.searchQuery === '' || this.searchQuery === this.q) return
    this.$router.push(`/search?q=${this.searchQuery}`)
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
    align-items: center;

    height: 56px;

    .panel-search {
      display: flex;
      align-items: center;
      position: relative;
      margin-left: 50px;
      width: 50%;

      &:before {
        display: block;
        position: absolute;
        left: 12px;
        font-family: 'Font Awesome 5 Free';
        font-weight: bold;
        content: '\f002';
      }

      input.searchbox {
        padding-left: 36px;
      }
    }

    .panel-ask {
      flex-grow: 1;
      margin-left: 50px;
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

.btn.btn-ask {
  font-size: 0.9em;
  white-space: pre;
}
</style>
