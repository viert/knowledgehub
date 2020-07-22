import { wrap } from './utils'
import Axios from 'axios'

const API_PREFIX = '/api/v1/search'

const Search = {
  Search(query: string, page = 1) {
    return wrap(Axios.get(`${API_PREFIX}/?q=${query}&_page=${page}`))
  }
}

export default Search
