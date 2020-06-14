<template>
  <form
    @submit.prevent="handleSave"
    class="shadow-block floating-block username_picker"
  >
    <div class="form-group">
      <username-suggest ref="usernameInput" v-model="username" />
    </div>
    <div>
      <button @click="handleSave" class="btn btn-sm btn-primary"
        >Добавить</button
      >
    </div>
  </form>
</template>

<script>
import UsernameSuggest from './UsernameSuggest'
export default {
  data() {
    return {
      username: ''
    }
  },
  components: {
    UsernameSuggest
  },
  mounted() {
    this.$refs.usernameInput.focus()
  },
  methods: {
    handleSave() {
      this.$emit('add', this.username)
    }
  }
}
</script>
