import { Module } from 'vuex'
import { RootState, QuestionsState, Question, Answer, Comment } from './types'
import Api from '@/api'

class MaxPage extends Error {
  maxPage: number

  constructor(maxPage: number) {
    super('maximum page number exceeded')
    this.maxPage = maxPage
  }
}

const questionsStore: Module<QuestionsState, RootState> = {
  namespaced: true,
  state: {
    questionList: [],
    question: null,
    answers: [],
    comments: [],
    page: 1,
    totalPages: 1
  },
  getters: {
    isMyQuestion(state, _, rootState) {
      return state.question?.author_id === rootState.users.user?._id
    }
  },
  mutations: {
    storeQuestionsList(state, questions: Array<Question>) {
      state.questionList = questions
    },
    setPage(state, page: number) {
      state.page = page
    },
    setTotalPages(state, totalPages: number) {
      state.totalPages = totalPages
    },
    storeQuestion(state, question: Question) {
      state.question = question
    },
    storeAnswers(state, answers: Array<Answer>) {
      state.answers = answers
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
    storeComments(state, comments: Array<Comment>) {
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
    }
  },
  actions: {
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
    }
  }
}

export default questionsStore
