<template>
  <a :href="provider.authorize_uri" :class="btnClass">
    <i v-if="provider.fa_icon" :class="provider.fa_icon"></i>
    {{ provider.provider_name }}
  </a>
</template>

<script>
export default {
  props: {
    provider: {
      type: Object,
      required: true
    }
  },
  computed: {
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
