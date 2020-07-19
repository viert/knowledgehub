import { wrap } from './utils'
import Axios from 'axios'

const Answers = (questionId: string) => {
  const prefix = `/api/v1/questions/${questionId}/answers`
  return {
    Create(body: string) {
      return wrap(Axios.post(`${prefix}/`, { body }))
    },
    Vote(answerId: string, value: 1 | 0 | -1) {
      return wrap(Axios.post(`${prefix}/${answerId}/vote`, { value }))
    },
    Accept(answerId: string) {
      return wrap(Axios.post(`${prefix}/${answerId}/accept`))
    },
    Revoke(answerId: string) {
      return wrap(Axios.post(`${prefix}/${answerId}/revoke`))
    }
  }
}

export default Answers