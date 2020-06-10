import Axios from 'axios'
import { wrap } from './utils'
import Account from './account'
import Questions from './questions'
import Users from './users'

const Api = {
  Account,
  Questions,
  Users,
  AppInfo() {
    return wrap(Axios.get('/app_info'))
  }
}

export default Api
