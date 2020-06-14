<template>
  <div class="page-layout">
    <main v-if="loggedIn">
      <div class="ask">
        <h3 class="page-title">Ask Question</h3>
        <MarkdownEditor v-model="body"></MarkdownEditor>
        <div class="preview">
          <h4>Preview</h4>
          <div class="preview-inner">
            <Post :body="body" />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { AuthStates } from '@/constants'
import { mapState } from 'vuex'
import MarkdownEditor from '@/components/Editors/MarkdownEditor'
import Post from '@/components/Post'

export default {
  data() {
    return {
      body: ''
    }
  },
  components: {
    MarkdownEditor,
    Post
  },
  computed: {
    ...mapState({
      authState: state => state.users.authState
    }),
    loggedIn() {
      return this.authState === AuthStates.LoggedIn
    }
  },
  mounted() {
    this.checkAuthState()
  },
  methods: {
    checkAuthState() {
      if (this.authState === AuthStates.LoggedOut) {
        this.$router.replace('/signin')
      }
    }
  },
  watch: {
    authState() {
      this.checkAuthState()
    }
  }
}
</script>

<style lang="scss">
.ask {
  padding: 20px;

  .preview {
    background: #eeeeee;
    padding: 8px;
    margin-top: 1em;
    h4 {
      font-family: Montserrat;
    }
    .preview-inner {
      padding: 8px;
      background: white;
    }
  }
}
</style>
