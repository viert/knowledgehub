import { RootState, TagsState, Tag } from './types'
import { Module } from 'vuex'
import Api from '@/api'

function defaultTag(tagName: string): Tag {
  return {
    name: tagName,
    description: `Questions related to ${tagName}`,
    questions_count: 1,
    subscribers_count: 0
  }
}

const tagsStore: Module<TagsState, RootState> = {
  state: {
    tags: {},
    tagLoaders: {}
  },
  mutations: {
    setTag(state, tag: Tag) {
      state.tags = {
        ...state.tags,
        [tag.name]: tag
      }
    },
    setTagLoader(state, payload: { tagName: string; promise: Promise<Tag> }) {
      const { tagName, promise } = payload
      state.tagLoaders = {
        ...state.tagLoaders,
        [tagName]: promise
      }
    },
    resetTagLoader(state, tagName: string) {
      const loaderKeys = Object.keys(state.tagLoaders)

      state.tagLoaders = loaderKeys.reduce<{ [key: string]: Promise<Tag> }>(
        (acc, item) => {
          if (item !== tagName) {
            acc[item] = state.tagLoaders[item]
          }
          return acc
        },
        {}
      )
    }
  },
  actions: {
    lazyLoadTag({ state, commit }, tagName) {
      if (state.tags[tagName]) return Promise.resolve(state.tags[tagName])
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

export default tagsStore
