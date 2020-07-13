import Axios from 'axios'
import { wrap } from './utils'
import Account from './account'
import Questions from './questions'
import Answers from './answers'
import Users from './users'
import Tags from './tags'

const Api = {
  Account,
  Questions,
  Answers,
  Users,
  Tags,
  AppInfo() {
    return wrap(Axios.get('/app_info'))
  }
}

export default Api
