<template>
  <form
    @submit.prevent="handleSave"
    class="shadow-block floating-block username_picker"
  >
    <div class="form-group">
      <username-suggest
        ref="usernameInput"
        v-model="username"
        @escape="$emit('close')"
      />
    </div>
    <div>
      <button @click="handleSave" class="btn btn-sm btn-primary">Add</button>
    </div>
  </form>
</template>

<script lang="ts">
import { Vue, Component, Emit } from 'vue-property-decorator'
import UsernameSuggest from './UsernameSuggest.vue'

@Component({
  components: {
    UsernameSuggest
  }
})
export default class UsernamePicker extends Vue {
  private username = ''

  mounted() {
    const input = this.$refs.usernameInput as HTMLInputElement
    input.focus()
  }

  @Emit('add')
  handleSave() {
    return this.username
  }
}
</script>
