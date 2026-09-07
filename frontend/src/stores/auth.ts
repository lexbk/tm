import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { authApi } from '../api/auth'
import type { LoginPayload } from '../types/api'

export const useAuthStore = defineStore(
  'auth',
  () => {
    const accessToken = ref(
      localStorage.getItem('access_token')
    )

    const refreshToken = ref(
      localStorage.getItem('refresh_token')
    )

    const username = ref(
      localStorage.getItem('username') || ''
    )

    const isAuthenticated = computed(
      () => !!accessToken.value
    )

    async function login(
      payload: LoginPayload
    ) {
      const { data } =
        await authApi.login(payload)

      accessToken.value = data.access
      refreshToken.value = data.refresh
      username.value = payload.username

      localStorage.setItem(
        'access_token',
        data.access
      )

      localStorage.setItem(
        'refresh_token',
        data.refresh
      )

      localStorage.setItem(
        'username',
        payload.username
      )
    }

    function logout() {
      accessToken.value = null
      refreshToken.value = null
      username.value = ''

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('username')
    }

    return {
      accessToken,
      refreshToken,
      username,
      isAuthenticated,
      login,
      logout
    }
  }
)
