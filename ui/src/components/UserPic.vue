<template>
  <div class="userpic">
    <img :src="src" />
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component
export default class UserPic extends Vue {
  @Prop({ type: String, default: '' }) readonly url!: string
  get src() {
    return this.url === '' ? '/images/user.jpeg' : this.url
  }
}
</script>

<style lang="scss">
$userpic_size: 48px;

.userpic {
  width: $userpic_size;
  height: $userpic_size;
  border-radius: 50%;
  border: 1px solid #999999;
  overflow: hidden;
  img {
    width: $userpic_size - 2;
    height: $userpic_size - 2;
  }
}
</style>
