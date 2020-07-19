<template>
  <div class="signin-page">
    <div class="signin">
      <h3>Sign in with...</h3>
      <ProviderButton
        v-for="provider in providers"
        :key="provider.provider_name"
        :provider="provider"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { ProviderInfo } from '../../store/types'
import ProviderButton from './ProviderButton.vue'

const users = namespace('users')

@Component({ components: { ProviderButton } })
export default class SigninPage extends Vue {
  @users.State('providers') readonly providers!: ProviderInfo[]
}
</script>

<style lang="scss">
.signin-page {
  min-height: calc(100vh - 128px);
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  .signin {
    width: 400px;
    margin: auto;
    height: 400px;
    background: white;
    border: 1px solid #cccccc;
    padding: 20px;

    h3 {
      margin-bottom: 40px;
    }
  }
}
</style>
