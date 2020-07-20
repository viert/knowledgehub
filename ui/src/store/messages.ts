import { Module } from 'vuex'
import { MessagesState, RootState, Message } from './types'

const DEFAULT_ALERT_TTL = 8000

const TYPE2CLASS = {
  alert: 'alert-danger',
  error: 'alert-danger',
  info: 'alert-info',
  warning: 'alert-warning',
  success: 'alert-success'
}

const messagesStore: Module<MessagesState, RootState> = {
  namespaced: true,
  state: {
    messages: []
  },
  mutations: {
    pushMessage(state, msg: Message) {
      state.messages = [...state.messages, msg]
    },
    popMessage(state, msgId: number) {
      state.messages = state.messages.filter(item => item.id !== msgId)
    }
  },
  actions: {
    addMessage({ commit }, msg: Message) {
      if (!msg.id) {
        msg.id = new Date().getTime()
      }

      if (!msg.timeout) {
        msg.timeout = DEFAULT_ALERT_TTL
      }

      if (!msg.type) {
        msg.type = 'info'
      }

      msg.classes = TYPE2CLASS[msg.type]

      msg.tm = setTimeout(() => {
        commit('popMessage', msg.id)
      }, msg.timeout)
      commit('pushMessage', msg)
    },
    removeMessage({ commit, state }, msgId) {
      const msg = state.messages.find(item => item.id === msgId)
      if (!msg) {
        return
      }
      clearTimeout(msg.tm)
      commit('popMessage', msgId)
    },
    alert({ dispatch }, text: string) {
      dispatch('addMessage', { type: 'error', text })
    },
    error({ dispatch }, text: string) {
      dispatch('addMessage', { type: 'error', prefix: 'Error:', text })
    },
    info({ dispatch }, text: string) {
      dispatch('addMessage', { type: 'info', text })
    },
    warning({ dispatch }, text: string) {
      dispatch('addMessage', { type: 'warning', text })
    },
    success({ dispatch }, text: string) {
      dispatch('addMessage', { type: 'success', text })
    }
  }
}

export default messagesStore
