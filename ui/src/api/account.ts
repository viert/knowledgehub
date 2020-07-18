import Axios from 'axios'
import { wrap } from './utils'
import { UserSettings } from './types'
import { User } from '@/types'

const API_PREFIX = '/api/v1/account'

const Account = {
  Me(noIntercept: boolean) {
    const request = Axios.get(`${API_PREFIX}/me`)
    if (noIntercept) {
      return request
    }
    return wrap(request)
  },
  Update(settings: UserSettings) {
    return wrap(Axios.patch(`${API_PREFIX}/me`, settings))
  },
  Logout() {
    return Axios.post(`${API_PREFIX}/logout`)
  }
}

export default Account
