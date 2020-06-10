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
  }
}

export default Questions
