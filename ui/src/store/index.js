import Vue from 'vue'
import Vuex from 'vuex'
import UsersStore from './users'
import MessagesStore from './messages'
import QuestionsStore from './questions'
import DataStore from './data'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    data: DataStore,
    messages: MessagesStore,
    users: UsersStore,
    questions: QuestionsStore
  }
})
