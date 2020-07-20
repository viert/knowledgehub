import { wrap } from './utils'
import Axios from 'axios'

const Users = {
  GetMany(userIds: Array<string>) {
    if (!(userIds instanceof Array)) {
      userIds = [userIds]
    }
    return wrap(Axios.get(`/api/v1/users/${userIds.join(',')}`))
  },
  Suggest(prefix: string) {
    return wrap(Axios.get(`/api/v1/users/suggest?prefix=${prefix}`))
  }
}

export default Users
