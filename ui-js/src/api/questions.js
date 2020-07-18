import { wrap } from './utils'
import Axios from 'axios'

const API_PREFIX = '/api/v1/questions'

const Questions = {
  List(page = 1, limit = 10, options) {
    const { sort } = options
    const url = `${API_PREFIX}/?_page=${page}&_limit=${limit}&_sort=${sort}`
    return wrap(Axios.get(url))
  },
  Get(questionId) {
    const url = `${API_PREFIX}/${questionId}`
    return wrap(Axios.get(url))
  },
  Create(title, body, tags) {
    const payload = { title, body, tags }
    return wrap(Axios.post(`${API_PREFIX}/`, payload))
  },
  Vote(questionId, value) {
    return wrap(Axios.post(`${API_PREFIX}/${questionId}/vote`, { value }))
  }
}

export default Questions
