import Api from '@/api'

class MaxPage extends Error {
  constructor(maxPage) {
    super('maximum page number exceeded')
    this.maxPage = maxPage
  }
}

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
    addAnswer(state, answer) {
      answer = {
        ...answer,
        flash: true
      }
      state.answers = [...state.answers, answer]
    },
    addComment(state, comment) {
      comment = {
        ...comment,
        flash: true
      }
      state.comments = [...state.comments, comment]
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
    getQuestion({ commit }, questionId) {
      return Api.Questions.Get(questionId).then(response => {
        const { question, answers, comments, authors } = response.data.data
        commit('storeQuestion', question)
        commit('storeAnswers', answers)
        commit('storeComments', comments)
        commit('users/applyUsers', authors, { root: true })
        return response
      })
    },
    createAnswer({ state, commit }, body) {
      return Api.Answers(state.question._id)
        .Create(body)
        .then(response => {
          commit('addAnswer', response.data.data)
          return response.data.data._id
        })
    },
    createQuestionComment({ state, commit }, body) {
      return Api.Comments(state.question._id)
        .Create(body)
        .then(response => {
          commit('addComment', response.data.data)
          return response.data.data._id
        })
    }
  }
}

export default QuestionsStore
