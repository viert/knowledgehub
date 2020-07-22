import { AuthState } from '@/constants'

export interface User {
  _id: string
  username: string
  first_name: string
  last_name: string
  ext_id: string
  email: string
  avatar_url: string
  telegram_id: string
  icq_id: string
  notify_by_email: boolean
  notify_by_telegram: boolean
  notify_by_icq: boolean
}

export interface Question {
  _id: string
  body: string
  title: string
  tags: string[]
  author_id: string
  answers_count: number
  has_accepted_answer: boolean
  type?: 'question'
}

export interface Answer {
  _id: string
  body: string
  parent_id: string
  accepted: boolean
  author_id: string
  flash?: boolean
  type?: 'answer'
}

export interface Comment {
  _id: string
  body: string
  parent_id: string
  author_id: string
  flash?: boolean
  type?: 'comment'
}

export interface Tag {
  name: string
  description: string
  questions_count: number
  subscribers_count: number
}

export interface Message {
  id?: number
  timeout?: number
  type: 'alert' | 'error' | 'info' | 'warning' | 'success'
  tm?: number
  classes?: string
  text: string
}

interface MongoDBShardInfo {
  allocator: string
  bits: number
  debug: boolean
  gitVersion: string
  javascriptEngine: string
  maxBsonObjectSize: number
  modules: string[]
  ok: number
  openssl: {
    running: string
  }
  storageEngines: string[]
  sysInfo: string
  version: string
  versionArray: number[]
}

interface MongoDBInfo {
  meta: MongoDBShardInfo
  shards: { [key: string]: MongoDBShardInfo }
}

export interface AppInfo {
  app: {
    name: string
    version: string
  }
  cache: {
    active: boolean
    type: string
  }
  mongodb: MongoDBInfo
}

export interface ProviderInfo {
  authorize_uri: string
  btn_class: string
  fa_icon: string
  provider_name: string
}

export interface UsersState {
  user: User | null
  tagSubscriptions: string[]
  userSubscriptions: string[]
  providers: ProviderInfo[]
  authState: AuthState
  signinOrigin: string
  users: { [key: string]: User }
  loadingUsers: {
    [key: string]: { promise: Promise<User>; resolver: Function }
  }
}

export interface QuestionsState {
  questionsList: Question[]
  searchResults: Array<Question | Answer>
  question: Question | null
  answers: Answer[]
  comments: Comment[]
  page: number
  totalPages: number
  count: number
}

export interface DataState {
  appInfo: AppInfo | null
}

export interface TagsState {
  tags: { [key: string]: Tag }
  tagLoaders: { [key: string]: Promise<Tag> }
}

export interface MessagesState {
  messages: Message[]
}

export interface RootState {
  users: UsersState
  questions: QuestionsState
  data: DataState
}
