import Api from '@/api'

const QuestionsStore = {
  namespaced: true,
  state: {
    questionsList: [],
    question: {},
    answers: [],
    comments: [],
    page: 1,
    totalPages: 1
  },
  mutations: {
    storeQuestionsList(state, questions) {
      state.questionsList = questions
    },
    setPage(state, page) {
      state.page = page
    },
    setTotalPages(state, totalPages) {
      state.totalPages = totalPages
    },
    storeQuestion(state, question) {
      state.question = question
    },
    storeAnswers(state, answers) {
      state.answers = answers
    },
    storeComments(state, comments) {
      state.comments = comments
    }
  },
  actions: {
    loadQuestions({ commit }, payload) {
      const { page, sort, limit } = payload
      return Api.Questions.List(page, limit, { sort }).then(response => {
        const { questions, authors } = response.data
        commit('storeQuestionsList', questions.data)
        commit('setPage', questions.page)
        commit('setTotalPages', questions.total_pages)
        commit('users/applyUsers', authors.data, { root: true })
      })
    },
    getQuestion({ commit }, questionId) {
      return Api.Questions.Get(questionId).then(response => {
        const { question, answers, comments, authors } = response.data.data
        commit('storeQuestion', question)
        commit('storeAnswers', answers)
        commit('storeComments', comments)
        commit('users/applyUsers', authors, { root: true })
        return response
      })
    }
  }
}

export default QuestionsStore
