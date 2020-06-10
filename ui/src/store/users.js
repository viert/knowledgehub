import Api from '@/api'
import { AuthStates } from '@/constants'

function storeUser(state, user) {
  state.users = {
    ...state.users,
    [user.username]: user,
    [user._id]: user
  }
}

const UsersStore = {
  namespaced: true,
  state: {
    user: {},
    oauthUrl: null,
    authState: 'unknown',
    users: {},
    loadingUsers: {}
  },
  getters: {
    me: state => state.user,
    user: state => id => {
      return state.users[id]
    }
  },
  mutations: {
    setAuthState(state, payload) {
      state.authState = payload
    },
    setCurrentUser(state, user) {
      state.user = user
      storeUser(state, user)
    },
    setOAuthURL(state, url) {
      state.oauthUrl = url
    },
    setUser(state, user) {
      storeUser(state, user)
    },
    applyUsers(state, users) {
      users.forEach(user => {
        storeUser(state, user)
      })
    },
    setUserLoading(state, payload) {
      const { username, request } = payload
      state.loadingUsers[username] = request
    },
    removeUserLoading(state, userId) {
      const users = {
        ...state.loadingUsers
      }
      delete users[userId]
      state.loadingUsers = users
    }
  },
  actions: {
    loadAuthInfo({ commit }) {
      return Api.Account.Me(true)
        .then(response => {
          commit('setCurrentUser', response.data.data)
          commit('setOAuthURL', response.data.oauth)
          commit('setAuthState', AuthStates.LoggedIn)
        })
        .catch(err => {
          if (err.response && err.response.status === 401) {
            commit('setCurrentUser', null)
            commit('setAuthState', AuthStates.LoggedOut)
            const { data } = err.response
            if (data && data.oauth) commit('setOAuthURL', data.oauth)
          }
        })
    },
    login({ commit }, { username, password }) {
      return Api.Account.Authenticate(username, password).then(response => {
        commit('setCurrentUser', response.data.data)
        commit('setAuthState', AuthStates.LoggedIn)
      })
    },
    logout({ commit, dispatch }) {
      return Api.Account.Logout().then(() => {
        commit('setCurrentUser', null)
        commit('setAuthState', AuthStates.LoggedOut)
        dispatch('messages/info', 'logged out', { root: true })
      })
    },

    lazyLoadUser({ commit, state }, userId) {
      if (userId in state.users) {
        return Promise.resolve(state.users[userId])
      }
      if (userId in state.loadingUsers) {
        return state.loadingUsers[userId]
      }
      const request = Api.Users.Get(userId)
        .then(response => {
          const user = response.data.data
          commit('setUser', user)
          return user
        })
        .finally(() => {
          commit('removeUserLoading', userId)
        })
      commit('setUserLoading', { userId, request })
      return request
    }
  }
}

export default UsersStore
