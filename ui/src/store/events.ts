import { Module } from 'vuex'
import {
  EventsState,
  RootState,
  AnyEvent,
  MaxPage,
  BotDescription
} from './types'
import Api from '@/api'

const eventsStore: Module<EventsState, RootState> = {
  namespaced: true,
  state: {
    eventsList: null,
    bots: {},
    page: 1,
    totalPages: 0,
    count: 0,
    loading: false
  },
  mutations: {
    clearEvents(state) {
      state.eventsList = []
    },
    storeEvents(state, events: AnyEvent[]) {
      state.eventsList = events
    },
    setPage(state, page: number) {
      state.page = page
    },
    setLoading(state, value: boolean) {
      state.loading = value
    },
    setTotalPages(state, totalPages: number) {
      state.totalPages = totalPages
    },
    setCount(state, count: number) {
      state.count = count
    },
    removeEvent(state, eventId: string) {
      state.eventsList = state.eventsList.filter(item => item._id !== eventId)
    },
    storeBots(state, botList: BotDescription[]) {
      state.bots = botList.reduce(
        (acc: { [key: string]: BotDescription }, botDesc) => {
          acc[botDesc.network_type] = botDesc
          return acc
        },
        {}
      )
    }
  },
  actions: {
    async loadBots({ commit }) {
      console.log('loading bots')
      return Api.Events.BotList().then(response => {
        commit('storeBots', response.data.bots)
      })
    },
    async loadEvents({ commit }, page: number) {
      commit('clearEvents')
      commit('setLoading', true)
      return Api.Events.List(page)
        .then(({ data }) => {
          if (data.total_pages > 0 && data.page > data.total_pages) {
            // fixpage
            throw new MaxPage(data.total_pages)
          }
          commit('storeEvents', data.data)
          commit('setTotalPages', data.total_pages)
          commit('setCount', data.count)
          commit('setPage', data.page)
        })
        .finally(() => {
          commit('setLoading', false)
        })
    },
    async dismiss({ commit }, eventId: string) {
      return Api.Events.Dismiss(eventId).then(() => {
        commit('removeEvent', eventId)
      })
    },
    async dismissAll({ commit }) {
      return Api.Events.DismissAll().then(() => {
        commit('clearEvents')
      })
    }
  }
}

export default eventsStore
