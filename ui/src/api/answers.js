import { wrap } from './utils'
import Axios from 'axios'

const Answers = questionId => {
  const prefix = `/api/v1/questions/${questionId}/answers`
  return {
    Create(body) {
      return wrap(Axios.post(`${prefix}/`, { body }))
    },
    Vote(answerId, value) {
      return wrap(Axios.post(`${prefix}/${answerId}/vote`, { value }))
    },
    Accept(answerId) {
      return wrap(Axios.post(`${prefix}/${answerId}/accept`))
    },
    Revoke(answerId) {
      return wrap(Axios.post(`${prefix}/${answerId}/revoke`))
    }
  }
}

export default Answers
