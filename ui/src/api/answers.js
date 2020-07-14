import { wrap } from './utils'
import Axios from 'axios'

const Answers = questionId => {
  const prefix = `/api/v1/questions/${questionId}/answers`
  return {
    Create(body) {
      return wrap(Axios.post(`${prefix}/`, { body }))
    }
  }
}

export default Answers
