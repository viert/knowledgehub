<template>
  <div class="author_card">
    <div class="author_card-asked">{{ action }} {{ askedAt | duration }}</div>
    <div class="author_card-userinfo">
      <UserPic :url="author.avatar_url" />
      <User :id="author._id" />
    </div>
  </div>
</template>

<script>
import UserPic from '@/components/UserPic'
export default {
  components: {
    UserPic
  },
  props: {
    askedAt: {
      type: String,
      required: true
    },
    action: {
      type: String,
      default: ''
    },
    author: {
      type: Object,
      required: true
    }
  }
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
