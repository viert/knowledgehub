import store from '@/store'
import { AuthStates } from '@/constants'

const ErrorHandler = err => {
  if (err.response) {
    switch (err.response.status) {
      case 401:
        if (err.response.data && err.response.data.state === 'logged out') {
          store.commit('user/setAuthState', AuthStates.NotLoggedIn)
          store.commit('user/setUser', null)
          store.commit('user/setProviders', err.response.data.providers)
        }
        break

      case 404:
        return err.response
      case 502:
      case 504:
        store.commit('user/setAuthState', AuthStates.Maintenance)
        return
      default:
        if (err.response.data) {
          if (err.response.data.error) {
            store.dispatch('messages/error', err.response.data.error)
          } else {
            store.dispatch('messages/error', err.response.data)
          }
        } else {
          store.dispatch('messages/error', err.response.statusText)
        }
    }
    return err.response
  }
  window.console.error(err)
  return undefined
}

export const wrap = axiosRequest => {
  return new Promise((resolve, reject) => {
    axiosRequest
      .then(response => {
        if (response.data && response.data.message) {
          store.dispatch('messages/info', response.data.message)
        }
        resolve(response)
      })
      .catch(err => {
        reject(ErrorHandler(err))
      })
  })
}
