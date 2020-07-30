import { wrap } from './utils'
import Axios from 'axios'

const API_PREFIX = '/api/v1/questions'

const Questions = {
  List(page = 1, limit = 10, options: { sort: string }) {
    const { sort } = options
    const url = `${API_PREFIX}/?_page=${page}&_limit=${limit}&_sort=${sort}`
    return wrap(Axios.get(url))
  },
  Get(questionId: string) {
    const url = `${API_PREFIX}/${questionId}`
    return wrap(Axios.get(url))
  },
  Edit(
    questionId: string,
    payload: {
      title: string
      body: string
      tags: string[]
    }
  ) {
    const url = `${API_PREFIX}/${questionId}`
    return wrap(Axios.patch(url, payload))
  },
  Create(title: string, body: string, tags: Array<string>) {
    const payload = { title, body, tags }
    return wrap(Axios.post(`${API_PREFIX}/`, payload))
  },
  Vote(questionId: string, value: 1 | 0 | -1) {
    return wrap(Axios.post(`${API_PREFIX}/${questionId}/vote`, { value }))
  },
  Delete(questionId: string) {
    const url = `${API_PREFIX}/${questionId}`
    return wrap(Axios.delete(url))
  },
  Restore(questionId: string) {
    const url = `${API_PREFIX}/${questionId}/restore`
    return wrap(Axios.post(url))
  }
}

export default Questions
