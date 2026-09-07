import api from './http'

import type {
  Comment,
  Paginated,
  Task,
  TaskPriority,
  TaskStatus
} from '../types/api'

export interface TaskFilters {
  status?: TaskStatus | ''
  priority?: TaskPriority | ''
  assignee_id?: string
  creator?: string
  due_date?: string
  ordering?: string
  limit?: number
  offset?: number
}

export interface TaskPayload {
  title: string
  description: string
  status: TaskStatus
  priority: TaskPriority
  assignee_id?: string | null
  due_date?: string | null
}

export const taskApi = {
  list: (params: TaskFilters = {}) =>
    api.get<Paginated<Task>>(
      '/api/v1/tasks/',
      { params }
    ),

  get: (id: string) =>
    api.get<Task>(
      `/api/v1/tasks/${id}/`
    ),

  create: (payload: TaskPayload) =>
    api.post<Task>(
      '/api/v1/tasks/',
      payload
    ),

  update: (
    id: string,
    payload: Partial<TaskPayload>
  ) =>
    api.patch<Task>(
      `/api/v1/tasks/${id}/`,
      payload
    ),

  remove: (id: string) =>
    api.delete(
      `/api/v1/tasks/${id}/`
    ),

  comments: (
    taskId: string,
    params?: {
      limit?: number
      offset?: number
    }
  ) =>
    api.get<Paginated<Comment>>(
      `/api/v1/tasks/${taskId}/comments/`,
      { params }
    ),

  addComment: (
    taskId: string,
    body: string
  ) =>
    api.post<Comment>(
      `/api/v1/tasks/${taskId}/comments/`,
      { body }
    ),

  updateComment: (
    taskId: string,
    id: string,
    body: string
  ) =>
    api.patch<Comment>(
      `/api/v1/tasks/${taskId}/comments/${id}/`,
      { body }
    ),

  removeComment: (
    taskId: string,
    id: string
  ) =>
    api.delete(
      `/api/v1/tasks/${taskId}/comments/${id}/`
    )
}
