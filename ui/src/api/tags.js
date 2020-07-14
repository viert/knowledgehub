import { wrap } from './utils'
import Axios from 'axios'

const Tags = {
  Get(tagName) {
    return wrap(Axios.get(`/api/v1/tags/${tagName}`))
  },
  Subscribe(tagName) {
    return wrap(Axios.post(`/api/v1/tags/${tagName}/subscribe`))
  },
  Unsubscribe(tagName) {
    return wrap(Axios.post(`/api/v1/tags/${tagName}/unsubscribe`))
  }
}

export default Tags
