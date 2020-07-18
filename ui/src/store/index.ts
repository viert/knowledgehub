import Vue from 'vue'
import Vuex from 'vuex'
import usersStore from './users'
import questionsStore from './questions'
import tagsStore from './tags'
import messagesStore from './messages'
import dataStore from './data'

Vue.use(Vuex)

export default new Vuex.Store({
  mutations: {},
  actions: {},
  modules: {
    users: usersStore,
    questions: questionsStore,
    tags: tagsStore,
    messages: messagesStore,
    data: dataStore
  }
})
