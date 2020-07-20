<template>
  <div class="suggest">
    <input
      ref="input"
      class="form-control"
      :class="{
        'form-control-sm': size === 'small',
        'is-valid': valid,
        'is-invalid': invalid
      }"
      type="text"
      placeholder="Type a user name"
      :value="value"
      :readonly="readonly"
      @keydown="handleKeydown"
      @input="handleInput"
    />
    <ul v-if="optionsOpen" class="suggest-list shadow-block">
      <li
        v-for="user in users"
        :key="user.username"
        @click="pickUser(user)"
        @mouseenter="handleListItemMouseEnter(user)"
        class="suggest-list-item"
        :class="{ active: user.active }"
      >
        <div class="suggest-username">{{ user.username }}</div>
        <div class="suggest-name"
          >{{ user.first_name }} {{ user.last_name }}</div
        >
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import _ from 'lodash'
import { Vue, Component, Prop } from 'vue-property-decorator'
import Api from '@/api'

interface UserItem {
  _id: string
  username: string
  first_name: string
  last_name: string
  active?: boolean
}

@Component
export default class UsernameSuggest extends Vue {
  @Prop({ type: String, required: true }) value!: string
  @Prop({ type: String, default: 'small' }) size!: string
  @Prop({ type: Boolean, default: false }) valid!: string
  @Prop({ type: Boolean, default: false }) invalid!: string
  @Prop({ type: Boolean, default: false }) readonly!: string

  private loadSoon: (() => void) | null = null
  private users: UserItem[] = []
  private optionsOpen = false

  created() {
    this.loadSoon = _.debounce(this.loadData, 150)
  }

  scrollActiveIntoViewSoon() {
    this.$nextTick(() => {
      if (document) {
        const item = document.querySelector('.suggest-list-item.active')
        if (item) {
          item.scrollIntoView({ block: 'center' })
        }
      }
    })
  }

  handleKeydown(e: KeyboardEvent) {
    let activeIdx = -1
    switch (e.keyCode) {
      case 38:
        activeIdx = this.users.findIndex(item => item.active)
        if (activeIdx > 0) {
          activeIdx--
          this.scrollActiveIntoViewSoon()
        }
        break
      case 40:
        activeIdx = this.users.findIndex(item => item.active)
        if (activeIdx < this.users.length - 1) {
          activeIdx++
          this.scrollActiveIntoViewSoon()
        }
        break
      case 13:
        e.preventDefault()
        activeIdx = this.users.findIndex(item => item.active)
        this.pickUser(this.users[activeIdx])
        return
      case 27:
        this.$emit('escape')
        return
    }
    if (activeIdx < 0) return
    this.users = this.users.map((item, idx) => {
      return {
        ...item,
        active: idx === activeIdx
      }
    })
  }

  handleInput(e: Event) {
    const input = e.target as HTMLInputElement
    this.$emit('input', input.value)
    this.loadSoon!()
  }

  loadData() {
    if (this.value === '') {
      this.users = []
      this.optionsOpen = false
      return
    }
    Api.Users.Suggest(this.value).then(response => {
      this.users = response.data.data.map((item: UserItem, index: number) => {
        return {
          ...item,
          active: index === 0
        }
      })
      this.optionsOpen = this.users.length > 0
    })
  }

  handleListItemMouseEnter(user: UserItem) {
    this.users = this.users.map(item => {
      return {
        ...item,
        active: item.username === user.username
      }
    })
  }

  pickUser(user: UserItem) {
    this.optionsOpen = false
    this.$emit('input', user.username)
  }

  focus() {
    const input = this.$refs.input as HTMLInputElement
    input.focus()
  }
}
</script>

<style lang="scss">
.suggest-list {
  .suggest-username {
    font-weight: bold;
  }
}
</style>
