<template>
  <a :href="authorizeURI" :class="btnClass">
    <i v-if="provider.fa_icon" :class="provider.fa_icon"></i>
    {{ provider.provider_name }}
  </a>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { ProviderInfo } from '@/store/types'

const users = namespace('users')

@Component
export default class ProviderButton extends Vue {
  @Prop({ type: Object, required: true }) readonly provider!: ProviderInfo
  @users.State('signinOrigin') origin!: string

  get authorizeURI() {
    const uri = new URL(this.provider.authorize_uri)
    const params = new URLSearchParams(uri.search)
    const state = `${params.get('state')}:${this.origin}`
    params.set('state', state)
    uri.search = params.toString()
    return uri.toString()
  }

  get btnClass() {
    let bc = 'btn btn-block btn-signin'
    if (this.provider.btn_class) {
      bc += ' ' + this.provider.btn_class
    }
    return bc
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
