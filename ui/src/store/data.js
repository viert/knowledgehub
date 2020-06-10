import Api from '@/api'

const DataStore = {
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

export default DataStore
