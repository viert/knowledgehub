import Api from '@/api'

function defaultTag(tagName) {
  return {
    name: tagName,
    description: `Questions related to ${tagName}`,
    questions_count: 1,
    subscribers_count: 0
  }
}

const TagsStore = {
  namespaced: true,
  state: {
    tags: {},
    tagLoaders: {}
  },
  getters: {
    getTag: state => tagName => {
      return state.tags[tagName]
    }
  },
  mutations: {
    setTag(state, tag) {
      state.tags = {
        ...state.tags,
        [tag.name]: tag
      }
    },
    setTagLoader(state, payload) {
      const { tagName, promise } = payload
      state.tagLoaders = {
        ...state.tagLoaders,
        [tagName]: promise
      }
    },
    resetTagLoader(state, tagName) {
      state.tagLoaders = Object.keys(state).reduce((acc, item) => {
        if (item !== tagName) {
          acc[item] = state.tagLoaders[item]
          return acc
        }
      }, {})
    }
  },
  actions: {
    lazyLoadTag({ state, commit }, tagName) {
      if (state.tags[tagName]) return Promise.resolve(state[tagName])
      if (state.tagLoaders[tagName]) return state.tagLoaders[tagName]
      const promise = Api.Tags.Get(tagName)
        .then(response => {
          const tag = response.data.data
          commit('setTag', tag)
          return tag
        })
        .catch(err => {
          if (err.status === 404) {
            const tag = defaultTag(tagName)
            commit('setTag', tag)
            return tag
          }
        })
        .finally(() => {
          commit('resetTagLoader', tagName)
        })
      commit('setTagLoader', { tagName, promise })
      return promise
    }
  }
}

export default TagsStore
