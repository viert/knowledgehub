import Axios from 'axios'
import { wrap } from './utils'

const API_PREFIX = '/api/v1/account'

const Account = {
  Me(noIntercept) {
    const request = Axios.get(`${API_PREFIX}/me`)
    if (noIntercept) {
      return request
    }
    return wrap(request)
  },
  Update(settings) {
    return wrap(Axios.patch(`${API_PREFIX}/me`, settings))
  },
  Logout() {
    return wrap(Axios.post(`${API_PREFIX}/logout`))
  }
}

export default Account
