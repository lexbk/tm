<script setup lang="ts">
import {
  useRoute,
  useRouter
} from 'vue-router'

import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div
    v-if="route.meta.auth"
    class="app-shell"
  >
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-mark">
          ✓
        </span>

        <span>Taskflow</span>
      </div>

      <nav>
        <RouterLink to="/tasks">
          Overview
        </RouterLink>
      </nav>

      <div class="sidebar-foot">
        <span class="avatar">
          {{
            auth.username
              .charAt(0)
              .toUpperCase() || 'U'
          }}
        </span>

        <div class="user">
          <b>
            {{ auth.username || 'User' }}
          </b>

          <small>
            Workspace member
          </small>
        </div>

        <button
          class="icon-btn"
          @click="logout"
          title="Sign out"
        >
          ↪
        </button>
      </div>
    </aside>

    <main class="main">
      <RouterView />
    </main>
  </div>

  <RouterView v-else />
</template>
