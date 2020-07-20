<template>
  <div class="signin">
    <h3>{{ message }}</h3>
    <ProviderButton
      v-for="provider in providers"
      :key="provider.provider_name"
      :provider="provider"
    />
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { ProviderInfo } from '../../store/types'
import ProviderButton from '@/components/SignIn/ProviderButton.vue'

const users = namespace('users')

@Component({ components: { ProviderButton } })
export default class SigninPage extends Vue {
  @Prop({ type: String, default: 'You must sign in to proceed...' })
  readonly message!: string
  @users.State('providers') readonly providers!: ProviderInfo[]
}
</script>

<style lang="scss"></style>
