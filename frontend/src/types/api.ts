export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE'

export type TaskPriority =
  | 'LOW'
  | 'MEDIUM'
  | 'HIGH'
  | 'URGENT'

export interface UserInfo {
  id: string
  username: string
}

export interface Task {
  id: string
  title: string
  description?: string
  status: TaskStatus
  priority: TaskPriority
  creator?: UserInfo
  assignee_id?: string | null
  assignee?: UserInfo | null
  due_date?: string | null
  created_at?: string
  updated_at?: string
}

export interface Comment {
  id: string
  body: string
  author: UserInfo
  created_at: string
  updated_at: string
}

export interface Paginated<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface TokenPair {
  access: string
  refresh: string
}

export interface LoginPayload {
  username: string
  password: string
}
