<template>
  <div class="alert-box">
    <transition-group name="message-list" tag="div">
      <div
        v-for="message in messages"
        :key="message.id"
        :class="`alert alert-dismissible ${message.classes}`"
      >
        <b>{{ message.prefix }}</b>
        {{ message.text }}
        <button @click="close(message.id)" type="button" class="close"
          >&times;</button
        >
      </div>
    </transition-group>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { Message } from '../store/types'

const messages = namespace('messages')

@Component
export default class AlertBox extends Vue {
  @messages.Action('removeMessage') close!: (msgId: string) => void
  @messages.State('messages') messages!: Message[]
}
</script>

<style lang="scss">
.alert-box {
  position: fixed;
  right: 14px;
  top: 70px;
  max-width: 80%;
  width: auto;
  z-index: 300;

  .alert {
    margin-bottom: 4px;
    width: max-content;
    margin-left: auto;
    &.alert-dismissible .close:hover {
      color: #fcfcfc;
    }
  }
}

.message-list-enter-active {
  animation: bounceInRight 0.5s linear;
}

.message-list-leave-active {
  animation: bounceOutRight 0.5s linear;
}
</style>
