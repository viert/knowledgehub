import { Module } from 'vuex'
import {
  RootState,
  QuestionsState,
  Question,
  Answer,
  Comment,
  MaxPage
} from './types'
import Api from '@/api'

const questionsStore: Module<QuestionsState, RootState> = {
  namespaced: true,
  state: {
    questionsList: [],
    question: null,
    answers: [],
    comments: [],
    searchResults: [],
    page: 1,
    totalPages: 0,
    count: 0
  },
  getters: {
    isMyQuestion(state, _, rootState) {
      return state.question?.author_id === rootState.users.user?._id
    },
    searchPageRelatedTags(state) {
      const tags = state.searchResults.reduce((acc, item) => {
        if (item.type === 'question') {
          const question = item as Question
          question.tags.forEach(tag => {
            acc.add(tag)
          })
        }
        return acc
      }, new Set<string>())
      return Array.from(tags)
    }
  },
  mutations: {
    storeQuestionsList(state, questions: Question[]) {
      state.questionsList = questions
    },
    setPage(state, page: number) {
      state.page = page
    },
    setTotalPages(state, totalPages: number) {
      state.totalPages = totalPages
    },
    setCount(state, count: number) {
      state.count = count
    },
    storeQuestion(state, question: Question) {
      state.question = question
    },
    storeAnswers(state, answers: Answer[]) {
      state.answers = answers
    },
    storeSearchResults(state, searchResults: Array<Answer | Question>) {
      state.searchResults = searchResults
    },
    addAnswer(state, answer: Answer) {
      answer = {
        ...answer,
        flash: true
      }
      state.answers = [...state.answers, answer]
    },
    addComment(state, comment: Comment) {
      comment = {
        ...comment,
        flash: true
      }
      state.comments = [...state.comments, comment]
    },
    storeComments(state, comments: Comment[]) {
      state.comments = comments
    },
    replaceComment(state, comment: Comment) {
      state.comments = state.comments.map(item => {
        return comment._id === item._id ? comment : item
      })
    },
    replaceAnswer(state, answer: Answer) {
      state.answers = state.answers.map(item => {
        return answer._id === item._id ? answer : item
      })
    },
    flashAnswer(state, answerId: string) {
      state.answers = state.answers.map(answer => {
        if (answer._id === answerId) {
          answer = {
            ...answer,
            flash: true
          }
        }
        return answer
      })
    },
    flashComment(state, commentId: string) {
      state.comments = state.comments.map(comment => {
        if (comment._id === commentId) {
          comment = {
            ...comment,
            flash: true
          }
        }
        return comment
      })
    }
  },
  actions: {
    async searchQuestions(
      { commit },
      payload: { page: number; query: string }
    ) {
      const { page, query } = payload
      return Api.Search.Search(query, page).then(response => {
        const { results, authors } = response.data
        if (results.total_pages > 0 && results.page > results.total_pages) {
          // fixpage
          throw new MaxPage(results.total_pages)
        }

        commit('storeSearchResults', results.data)
        commit('setPage', results.page)
        commit('setCount', results.count)
        commit('setTotalPages', results.total_pages)
        commit('users/applyUsers', authors.data, { root: true })
      })
    },
    async loadQuestions(
      { commit },
      payload: { page: number; sort: string; limit: number }
    ) {
      const { page, sort, limit } = payload
      return Api.Questions.List(page, limit, { sort }).then(response => {
        const { questions, authors } = response.data
        if (
          questions.total_pages > 0 &&
          questions.page > questions.total_pages
        ) {
          // fixpage
          throw new MaxPage(questions.total_pages)
        }
        commit('storeQuestionsList', questions.data)
        commit('setPage', questions.page)
        commit('setTotalPages', questions.total_pages)
        commit('users/applyUsers', authors.data, { root: true })
      })
    },
    async getQuestion({ commit }, questionId) {
      return Api.Questions.Get(questionId).then(response => {
        const { question, answers, comments, authors } = response.data.data
        commit('storeQuestion', question)
        commit('storeAnswers', answers)
        commit('storeComments', comments)
        commit('users/applyUsers', authors, { root: true })
        return response
      })
    },
    async createAnswer({ state, commit }, body) {
      if (!state.question) return

      return Api.Answers(state.question._id)
        .Create(body)
        .then(response => {
          commit('addAnswer', response.data.data)
          return response.data.data._id
        })
    },
    async createComment(
      { state, commit },
      payload: { parentId: string; body: string }
    ) {
      if (!state.question) return
      const { parentId, body } = payload

      // determine if it's a comment to a quesiton or one of its answers
      const api =
        parentId === state.question._id
          ? Api.Comments(state.question._id)
          : Api.Comments(state.question._id, parentId)

      return api.Create(body).then(response => {
        commit('addComment', response.data.data)
        return response.data.data._id
      })
    },
    async voteQuestion({ state, commit }, value: 1 | 0 | -1) {
      if (!state.question) return
      return Api.Questions.Vote(state.question._id, value).then(response => {
        commit('storeQuestion', response.data.data)
      })
    },
    async voteComment(
      { state, commit },
      payload: { commentId: string; value: 1 | 0 }
    ) {
      if (!state.question) return

      const { commentId, value } = payload
      const comment = state.comments.find(item => item._id === commentId)
      if (!comment) return

      const api =
        comment.parent_id === state.question._id
          ? Api.Comments(state.question._id)
          : Api.Comments(state.question._id, comment.parent_id)

      return api.Vote(comment._id, value).then(response => {
        commit('replaceComment', response.data.data)
      })
    },
    async voteAnswer(
      { state, commit },
      payload: { answerId: string; value: 1 | 0 | -1 }
    ) {
      if (!state.question) return

      const { answerId, value } = payload
      Api.Answers(state.question._id)
        .Vote(answerId, value)
        .then(response => {
          commit('replaceAnswer', response.data.data)
        })
    },
    async acceptAnswer({ state, commit }, answerId: string) {
      if (!state.question) return

      return Api.Answers(state.question._id)
        .Accept(answerId)
        .then(response => {
          commit('replaceAnswer', response.data.data)
        })
    },
    async revokeAnswer({ state, commit }, answerId) {
      if (!state.question) return

      return Api.Answers(state.question._id)
        .Revoke(answerId)
        .then(response => {
          commit('replaceAnswer', response.data.data)
        })
    },
    async deleteQuestion({ state, commit }) {
      if (!state.question) return

      return Api.Questions.Delete(state.question._id).then(response => {
        commit('storeQuestion', response.data.data)
      })
    },
    async restoreQuestion({ state, commit }) {
      if (!state.question) return

      return Api.Questions.Restore(state.question._id).then(response => {
        commit('storeQuestion', response.data.data)
      })
    },
    async deleteAnswer({ state, commit }, answerId) {
      if (!state.question) return

      return Api.Answers(state.question._id)
        .Delete(answerId)
        .then(response => {
          commit('replaceAnswer', response.data.data)
        })
    },
    async restoreAnswer({ state, commit }, answerId) {
      if (!state.question) return

      return Api.Answers(state.question._id)
        .Restore(answerId)
        .then(response => {
          commit('replaceAnswer', response.data.data)
        })
    },
    async editAnswer(
      { state, commit },
      payload: {
        answerId: number
        body: string
      }
    ) {
      if (!state.question) return

      return Api.Answers(state.question._id)
        .Edit(payload.body, payload.answerId)
        .then(response => commit('replaceAnswer', response.data.data))
    },
    async editQuestion({ state, commit }, payload) {
      if (!state.question) return

      return Api.Questions.Edit(state.question._id, payload).then(response => {
        commit('storeQuestion', response.data.data)
      })
    },
    async deleteComment({ state, commit }, commentId) {
      if (!state.question) return

      return Api.Comments(state.question._id)
        .Delete(commentId)
        .then(response => {
          commit('replaceComment', response.data.data)
        })
    },
    async restoreComment({ state, commit }, commentId) {
      if (!state.question) return

      return Api.Comments(state.question._id)
        .Restore(commentId)
        .then(response => {
          commit('replaceComment', response.data.data)
        })
    },
    async editCommentToQuestion(
      { state, commit },
      payload: {
        commentId: string
        body: string
      }
    ) {
      if (!state.question) return

      return Api.Comments(state.question._id)
        .Edit(payload.commentId, payload.body)
        .then(response => {
          commit('replaceComment', response.data.data)
        })
    },

    async editCommentToAnswer(
      { state, commit },
      payload: {
        commentId: string
        body: string
        answerId: string
      }
    ) {
      if (!state.question) return

      return Api.Comments(state.question._id, payload.answerId)
        .Edit(payload.commentId, payload.body)
        .then(response => {
          commit('replaceComment', response.data.data)
        })
    }
  }
}

export default questionsStore
