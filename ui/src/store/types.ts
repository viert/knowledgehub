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
}

export interface Answer {
  _id: string
  body: string
  parent_id: string
  accepted: boolean
  author_id: string
  flash?: boolean
}

export interface Comment {
  _id: string
  body: string
  parent_id: string
  author_id: string
  flash?: boolean
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

export interface UsersState {
  user: User | null
  userLoader: Promise<any> | null
  tagSubscriptions: string[]
  userSubscriptions: string[]
  providers: string[]
  authState: AuthState
  signinOrigin: string
  users: { [key: string]: User }
  loadingUsers: {
    [key: string]: { promise: Promise<User>; resolver: Function }
  }
}

export interface QuestionsState {
  questionList: Question[]
  question: Question | null
  answers: Answer[]
  comments: Comment[]
  page: number
  totalPages: number
}

export interface DataState {
  appInfo: { [key: string]: any }
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
