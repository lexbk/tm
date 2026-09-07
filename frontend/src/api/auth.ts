import api from './http'
import type {
  LoginPayload,
  TokenPair
} from '../types/api'

export const authApi = {
  login: (payload: LoginPayload) =>
    api.post<TokenPair>(
      '/api/v1/auth/token/',
      payload
    )
}
