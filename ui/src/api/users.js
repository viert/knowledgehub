import { wrap } from './utils'
import Axios from 'axios'

const Users = {
  Get(userId) {
    return wrap(Axios.get(`/api/v1/users/${userId}`))
  }
}

export default Users
