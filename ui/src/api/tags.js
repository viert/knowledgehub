import { wrap } from './utils'
import Axios from 'axios'

const Tags = {
  Get(tagName) {
    return wrap(Axios.get(`/api/v1/tags/${tagName}`))
  }
}

export default Tags
