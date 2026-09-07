<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function submit() {
  error.value = ''

  if (!username.value || !password.value) {
    error.value =
      'Username and password are required.'

    return
  }

  loading.value = true

  try {
    await auth.login({
      username: username.value,
      password: password.value
    })

    router.push('/tasks')
  } catch {
    error.value =
      'Invalid username or password.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="login-card">
      <div class="brand centered">
        <span class="brand-mark">
          ✓
        </span>

        <span>Taskflow</span>
      </div>

      <div class="auth-copy">
        <h1>
          Welcome back
        </h1>

        <p>
          Sign in to manage your tasks.
        </p>
      </div>

      <form
        @submit.prevent="submit"
      >
        <label>
          Username

          <input
            v-model="username"
            autocomplete="username"
            placeholder="Username"
          />
        </label>

        <label>
          Password

          <input
            v-model="password"
            type="password"
            autocomplete="current-password"
            placeholder="Password"
          />
        </label>

        <p
          v-if="error"
          class="error"
        >
          {{ error }}
        </p>

        <button
          class="btn primary wide"
          type="submit"
          :disabled="loading"
        >
          {{
            loading
              ? 'Signing in...'
              : 'Sign in'
          }}
        </button>
      </form>
    </div>
  </div>
</template>
