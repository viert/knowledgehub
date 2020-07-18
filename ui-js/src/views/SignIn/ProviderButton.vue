<template>
  <a :href="authorizeURI" :class="btnClass">
    <i v-if="provider.fa_icon" :class="provider.fa_icon"></i>
    {{ provider.provider_name }}
  </a>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    provider: {
      type: Object,
      required: true
    }
  },
  computed: {
    ...mapState({
      origin: state => state.users.signinOrigin
    }),
    authorizeURI() {
      const uri = new URL(this.provider.authorize_uri)
      const params = new URLSearchParams(uri.search)
      const state = `${params.get('state')}:${this.origin}`
      params.set('state', state)
      uri.search = params.toString()
      return uri.toString()
    },
    btnClass() {
      let bc = 'btn btn-block btn-signin'
      if (this.provider.btn_class) {
        bc += ' ' + this.provider.btn_class
      }
      return bc
    }
  }
}
</script>

<style lang="scss">
.btn-signin {
  font-size: 1em;
}

.btn-yandex {
  background: #ffdb4d;

  &:hover {
    background: #facf23;
  }
}
</style>
