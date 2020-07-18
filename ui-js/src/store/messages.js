const DEFAULT_ALERT_TTL = 8000

const TYPE2CLASS = {
  alert: 'alert-danger',
  error: 'alert-danger',
  info: 'alert-info',
  warning: 'alert-warning',
  success: 'alert-success'
}

const MessagesStore = {
  namespaced: true,
  state: {
    messages: []
  },
  getters: {},
  mutations: {
    pushMessage(state, msg) {
      state.messages.push(msg)
    },
    popMessage(state, msgId) {
      state.messages = state.messages.filter(item => item.id !== msgId)
    }
  },
  actions: {
    addMessage({ commit }, msg) {
      if (!msg.id) {
        msg.id = new Date() / 1
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
    alert({ dispatch }, text) {
      dispatch('addMessage', { type: 'error', text })
    },
    error({ dispatch }, text) {
      dispatch('addMessage', { type: 'error', prefix: 'Error:', text })
    },
    info({ dispatch }, text) {
      dispatch('addMessage', { type: 'info', text })
    },
    warning({ dispatch }, text) {
      dispatch('addMessage', { type: 'warning', text })
    },
    success({ dispatch }, text) {
      dispatch('addMessage', { type: 'success', text })
    }
  }
}

export default MessagesStore
