import { wrap } from './utils'
import Axios from 'axios'

const API_PREFIX = '/api/v1/events'

const Events = {
  List(page = 1) {
    return wrap(Axios.get(`${API_PREFIX}/?_page=${page}`))
  },
  Dismiss(eventId: string) {
    return wrap(Axios.post(`${API_PREFIX}/${eventId}/dismiss`))
  },
  DismissAll() {
    return wrap(Axios.post(`${API_PREFIX}/dismiss_all`))
  }
}

export default Events
