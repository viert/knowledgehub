<template>
  <div class="signin-page">
    <SigninBanner message="Sign in with..." />
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import SigninBanner from '@/components/SignIn/SigninBanner.vue'

@Component({ components: { SigninBanner } })
export default class SigninPage extends Vue {}
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
