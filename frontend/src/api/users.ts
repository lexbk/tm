import api from './http'

import type { Paginated, UserInfo } from '../types/api'

export const userApi = {
  list: (params: {
    limit?: number
    offset?: number
  } = {}) =>
    api.get<Paginated<UserInfo>>(
      '/api/v1/users/',
      { params }
    )
}
