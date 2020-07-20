import { wrap } from './utils'
import Axios from 'axios'

const Comments = (questionId: string, answerId: string | null = null) => {
  let prefix = `/api/v1/questions/${questionId}`
  if (answerId) {
    prefix += `/answers/${answerId}`
  }
  prefix += '/comments'

  return {
    Create(body: string) {
      return wrap(Axios.post(`${prefix}/`, { body }))
    },
    Vote(commentId: string, value: 1 | 0) {
      return wrap(Axios.post(`${prefix}/${commentId}/vote`, { value }))
    }
  }
}

export default Comments
