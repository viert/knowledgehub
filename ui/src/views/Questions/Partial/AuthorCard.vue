<template>
  <div class="author_card">
    <div class="author_card-asked">{{ action }} {{ askedAt | duration }}</div>
    <div class="author_card-userinfo">
      <UserPic :url="author.avatar_url" />
      <User :username="author.username" />
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import UserPic from '@/components/UserPic.vue'
import { User } from '@/store/types'

@Component({ components: { UserPic } })
export default class AuthorCard extends Vue {
  @Prop({ type: String, required: true }) readonly askedAt!: string
  @Prop({ type: String, default: '' }) readonly action!: string
  @Prop({ type: Object, required: true }) readonly author!: User
}
</script>

<style lang="scss">
.author_card {
  font-size: 0.8em;
  padding: 2px 8px;
  margin-bottom: 12px;

  &-asked {
    margin-bottom: 8px;
  }

  &-userinfo {
    display: flex;
    margin-bottom: 4px;
    .userpic {
      min-width: 48px;
      margin-right: 8px;
    }
  }
}
</style>
