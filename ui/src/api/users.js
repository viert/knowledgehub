import { wrap } from './utils'
import Axios from 'axios'

const Users = {
  GetMany(userIds) {
    if (!(userIds instanceof Array)) {
      userIds = [userIds]
    }
    return wrap(Axios.get(`/api/v1/users/${userIds.join(',')}`))
  }
}

export default Users
