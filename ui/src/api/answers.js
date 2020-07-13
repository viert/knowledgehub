import { wrap } from './utils'
import Axios from 'axios'

const Answers = questionId => ({
  Create(body) {
    return wrap(
      Axios.post(`/api/v1/questions/${questionId}/answers/`, { body })
    )
  }
})

export default Answers
