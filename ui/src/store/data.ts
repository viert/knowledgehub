import { DataState, RootState, AppInfo } from './types'
import { Module } from 'vuex'
import Api from '@/api'

const dataStore: Module<DataState, RootState> = {
  namespaced: true,
  state: {
    appInfo: null
  },
  mutations: {
    setAppInfo(state, appInfo: AppInfo) {
      state.appInfo = appInfo
    }
  },
  actions: {
    loadAppInfo({ commit, dispatch }) {
      dispatch('events/loadBots', null, { root: true })
      return Api.AppInfo().then(response => {
        commit('setAppInfo', response.data.app_info)
      })
    }
  }
}

export default dataStore
