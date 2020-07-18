import { DataState, RootState } from './types'
import { Module } from 'vuex'
import Api from '@/api'

const dataStore: Module<DataState, RootState> = {
  namespaced: true,
  state: {
    appInfo: {}
  },
  mutations: {
    setAppInfo(state, appInfo) {
      state.appInfo = appInfo
    }
  },
  actions: {
    loadAppInfo({ commit }) {
      return Api.AppInfo().then(response => {
        commit('setAppInfo', response.data.app_info)
      })
    }
  }
}

export default dataStore
