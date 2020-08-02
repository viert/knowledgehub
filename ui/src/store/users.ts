import { Module } from 'vuex'
import { RootState, UsersState, User } from './types'
import { AuthState } from '@/constants'
import Api from '@/api'

// this variable is holding a timeout handler
// when users bulk request is going to happen soon
let userLoader: number | null

function storeUser(state: UsersState, user: User) {
  state.users = {
    ...state.users,
    [user.username]: user,
    [user._id]: user
  }
}

function extractUserData(data: { [key: string]: any }): User {
  return {
    _id: data._id,
    avatar_url: data.avatar_url,
    ext_id: data.ext_id,
    first_name: data.first_name,
    last_name: data.last_name,
    username: data.username,
    email: data.email,
    telegram_id: data.telegram_id,
    icq_id: data.icq_id,
    moderator: data.moderator,
    tag_subscription: data.tag_subscription,
    user_subscription: data.user_subscription
  }
}

const usersStore: Module<UsersState, RootState> = {
  namespaced: true,
  state: {
    user: null,
    tagSubscriptions: [],
    userSubscriptions: [],
    providers: [],
    authState: AuthState.Unknown,
    signinOrigin: '/',
    users: {},
    loadingUsers: {}
  },
  getters: {
    me(state) {
      return state.user
    },
    user(state) {
      return (id: string) => {
        return state.users[id]
      }
    },
    authReady(state) {
      return (
        state.authState === AuthState.LoggedIn ||
        state.authState === AuthState.LoggedOut
      )
    }
  },
  mutations: {
    setAuthState(state, authState: AuthState) {
      state.authState = authState
    },
    setSigninOrigin(state, origin: string) {
      state.signinOrigin = origin
    },
    setCurrentUser(state, user: User) {
      state.user = user
      if (user) storeUser(state, user)
    },
    setProviders(state, providers) {
      state.providers = providers
    },
    setUser(state, user: User) {
      storeUser(state, user)
    },
    applyUsers(state, users: Array<User>) {
      users.forEach(user => {
        storeUser(state, user)
      })
    },
    setUserLoading(
      state,
      payload: { username: string; promise: Promise<User>; resolver: Function }
    ) {
      const { username, promise, resolver } = payload
      state.loadingUsers = {
        ...state.loadingUsers,
        [username]: { promise, resolver }
      }
    },
    setTagSubscriptions(state, tags: string[]) {
      state.tagSubscriptions = tags
    },
    setUserSubscriptions(state, users) {
      state.userSubscriptions = users
    },
    removeUserLoading(state, userId: string) {
      const users = {
        ...state.loadingUsers
      }
      delete users[userId]
      state.loadingUsers = users
    }
  },
  actions: {
    loadSubscriptionUsers({ commit }, userIds) {
      if (userIds.length === 0) return
      Api.Users.GetMany(userIds).then((response: any) => {
        commit('setUserSubscriptions', response.data.data)
      })
    },
    loadAuthInfo({ commit, dispatch }) {
      return Api.Account.Me(true)
        .then(response => {
          const { data } = response.data
          const tagSubscriptions = data.tag_subscription.tags
          const useridSubscriptions = data.user_subscription.subs_user_ids
          const userData = extractUserData(data)

          commit('setCurrentUser', userData)
          commit('setTagSubscriptions', tagSubscriptions)
          commit('setProviders', response.data.providers)
          commit('setAuthState', AuthState.LoggedIn)
          dispatch('loadSubscriptionUsers', useridSubscriptions)
        })
        .catch((err: any) => {
          if (err.response && err.response.status === 401) {
            commit('setCurrentUser', null)
            commit('setAuthState', AuthState.LoggedOut)
            commit('setProviders', err.response.data.providers)
          } else {
            throw err
          }
        })
    },
    subscribeToTag({ commit }, tag) {
      return Api.Tags.Subscribe(tag).then(response => {
        commit('setTagSubscriptions', response.data.data.tags)
      })
    },
    unsubscribeFromTag({ commit }, tag) {
      return Api.Tags.Unsubscribe(tag).then(response => {
        commit('setTagSubscriptions', response.data.data.tags)
      })
    },
    replaceTagSubscription({ commit }, tags) {
      return Api.Tags.Replace(tags).then(response => {
        commit('setTagSubscriptions', response.data.data.tags)
      })
    },
    logout({ commit, dispatch }) {
      return Api.Account.Logout().catch(err => {
        if (err.response && err.response.status === 401) {
          commit('setCurrentUser', null)
          commit('setAuthState', AuthState.LoggedOut)
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
        userLoader = setTimeout(() => {
          // loader itself
          const userIds = Object.keys(state.loadingUsers)
          Api.Users.GetMany(userIds)
            .then(response => {
              const users: User[] = response.data.data
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
      }
      // returning a resolver for user
      const p = new Promise(resolve => {
        commit('setUserLoading', {
          username: userId,
          promise: p,
          resolver: resolve
        })
      })
    },
    saveSettings({ commit }, settings) {
      return Api.Account.Update(settings).then(response => {
        const userData = extractUserData(response.data.data)
        commit('setCurrentUser', userData)
      })
    }
  }
}

export default usersStore
