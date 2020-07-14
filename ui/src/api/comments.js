import { wrap } from './utils'
import Axios from 'axios'

const Comments = (questionId, answerId = null) => {
  let prefix = `/api/v1/questions/${questionId}`
  if (answerId) {
    prefix += `/answers/${answerId}`
  }
  prefix += '/comments'

  return {
    Create(body) {
      return wrap(Axios.post(`${prefix}/`, { body }))
    }
  }
}

export default Comments
