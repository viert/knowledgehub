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

<script>
import Api from '@/api'
import _ from 'lodash'
export default {
  props: {
    value: {
      type: String,
      required: true
    },
    size: {
      type: String,
      default: 'small'
    },
    valid: {
      type: Boolean,
      default: false
    },
    invalid: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },
  created() {
    this.loadSoon = _.debounce(this.loadData, 150)
  },
  methods: {
    scrollActiveIntoViewSoon() {
      this.$nextTick(() => {
        document
          .querySelector('.suggest-list-item.active')
          .scrollIntoView({ block: 'center' })
      })
    },
    handleKeydown(e) {
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
    },
    handleInput(e) {
      this.$emit('input', e.target.value)
      this.loadSoon()
    },
    loadData() {
      if (this.value === '') {
        this.users = []
        this.optionsOpen = false
        return
      }
      Api.Users.Suggest(this.value).then(response => {
        this.users = response.data.data.map((item, index) => {
          return {
            ...item,
            active: index === 0
          }
        })
        this.optionsOpen = this.users.length > 0
      })
    },
    handleListItemMouseEnter(user) {
      this.users = this.users.map(item => {
        return {
          ...item,
          active: item.username === user.username
        }
      })
    },
    pickUser(user) {
      this.optionsOpen = false
      this.$emit('input', user.username)
    },
    focus() {
      this.$refs.input.focus()
    }
  },
  data() {
    return {
      users: [],
      optionsOpen: false
    }
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
