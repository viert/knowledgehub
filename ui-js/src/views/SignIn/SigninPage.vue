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

<script>
import { mapState } from 'vuex'
import ProviderButton from './ProviderButton'
export default {
  components: {
    ProviderButton
  },
  computed: {
    ...mapState({
      providers: state => state.users.providers
    })
  }
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
