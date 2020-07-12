import Api from '@/api'
import { AuthStates } from '@/constants'

function storeUser(state, user) {
  state.users = {
    ...state.users,
    [user.username]: user,
    [user._id]: user
  }
}

var userLoader = null

const UsersStore = {
  namespaced: true,
  state: {
    user: null,
    userLoader: null,
    providers: [],
    authState: AuthStates.Unknown,
    signinOrigin: '/',
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
    setSigninOrigin(state, origin) {
      state.signinOrigin = origin
    },
    setCurrentUser(state, user) {
      state.user = user
      if (user) storeUser(state, user)
    },
    setProviders(state, providers) {
      state.providers = providers
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
      const { username, promise, resolver } = payload
      state.loadingUsers = {
        ...state.loadingUsers,
        [username]: { promise, resolver }
      }
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
    setSigninOrigin({ commit }, origin) {
      commit('setSigninOrigin', origin)
    },
    loadAuthInfo({ commit }) {
      return Api.Account.Me(true)
        .then(response => {
          commit('setCurrentUser', response.data.data)
          commit('setProviders', response.data.providers)
          commit('setAuthState', AuthStates.LoggedIn)
        })
        .catch(err => {
          if (err.response && err.response.status === 401) {
            commit('setCurrentUser', null)
            commit('setAuthState', AuthStates.LoggedOut)
            commit('setProviders', err.response.data.providers)
          }
        })
    },
    logout({ commit, dispatch }) {
      return Api.Account.Logout().catch(err => {
        if (err.response && err.response.status === 401) {
          commit('setCurrentUser', null)
          commit('setAuthState', AuthStates.LoggedOut)
          dispatch('messages/info', 'logged out', { root: true })
        } else {
          throw err
        }
      })
    },
    lazyLoadUser({ commit, state }, userId) {
      if (userId in state.users) {
        return Promise.resolve(state.users[userId])
      }

      if (userId in state.loadingUsers) {
        return state.loadingUsers[userId].promise
      }

      if (userLoader === null) {
        // start loading users after a while
        // to be sure all the necessary users are
        // in a loading queue
        userLoader = new Promise((resolve, reject) => {
          setTimeout(() => {
            // loader itself
            const userIds = Object.keys(state.loadingUsers)
            Api.Users.GetMany(userIds)
              .then(response => {
                const users = response.data.data
                users.forEach(user => {
                  commit('setUser', user)
                  const nameResolver = state.loadingUsers[user.username]
                  if (nameResolver) {
                    nameResolver.resolver(user)
                  }
                  const idResolver = state.loadingUsers[user._id]
                  if (idResolver) {
                    idResolver.resolver(user)
                  }
                })
              })
              .finally(() => {
                userIds.forEach(userId => {
                  commit('removeUserLoading', userId)
                })
              })
            userLoader = null
          }, 20)
        })
      }
      // returning a resolver for user
      const p = new Promise(resolve => {
        commit('setUserLoading', {
          username: userId,
          promise: p,
          resolver: resolve
        })
      })
    }
  }
}

export default UsersStore
