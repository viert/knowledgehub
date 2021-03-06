import { AuthState } from '@/constants'

export class MaxPage extends Error {
  maxPage: number

  constructor(maxPage: number) {
    super('maximum page number exceeded')
    this.maxPage = maxPage
  }
}

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
  moderator: boolean
  tag_subscription: { tags: string[] }
  user_subscription: { subs_user_ids: string[] }
}

export interface Question {
  _id: string
  body: string
  title: string
  tags: string[]
  author_id: string
  answers_count: number
  deleted: boolean
  has_accepted_answer: boolean
  human_readable_id: string
  last_activity_at: Date
  type?: 'question'
}

export interface Answer {
  _id: string
  body: string
  parent_id: string
  accepted: boolean
  deleted: boolean
  author_id: string
  flash?: boolean
  type?: 'answer'
}

export interface Comment {
  _id: string
  body: string
  parent_id: string
  author_id: string
  deleted: boolean
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

export interface TagNewQuestionEvent {
  _id: string
  tags: string[]
  question_id: string
  question_human_readable_id: string
  question_title: string
  created_at: string
  type: 'tag_new_question_event'
}

export interface QuestionNewAnswerEvent {
  _id: string
  question_id: string
  question_title: string
  question_human_readable_id: string
  answer_id: string
  author_username: string
  created_at: string
  type: 'question_new_answer_event'
}

export interface PostNewCommentEvent {
  _id: string
  post_id: string
  post_type: 'question' | 'answer' | 'comment'
  root_id: string
  title: string
  comment_id: string
  created_at: string
  author_username: string
  type: 'post_new_comment_event'
}

export interface MentionEvent {
  _id: string
  post_id: string
  post_type: 'question' | 'answer' | 'comment'
  root_id: string
  author_username: string
  created_at: string
  type: 'mention_event'
}

export interface AnswerAcceptedEvent {
  _id: string
  answer_id: string
  accepted_by_username: string
  question_id: string
  created_at: string
  type: 'answer_accepted_event'
}

export type AnyEvent =
  | TagNewQuestionEvent
  | QuestionNewAnswerEvent
  | PostNewCommentEvent
  | MentionEvent
  | AnswerAcceptedEvent

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

export interface BotDescription {
  name: string
  link: string
  network_type: string
}

export interface EventsState {
  eventsList: AnyEvent[] | null
  bots: { icq?: BotDescription; telegram?: BotDescription }
  page: number
  totalPages: number
  count: number
  loading: boolean
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
