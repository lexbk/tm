import {
  createRouter,
  createWebHistory
} from 'vue-router'

import Login from '../pages/Login.vue'
import Dashboard from '../pages/Dashboard.vue'
import TaskDetail from '../pages/TaskDetail.vue'

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      redirect: '/tasks'
    },

    {
      path: '/login',
      name: 'login',
      component: Login
    },

    {
      path: '/tasks',
      name: 'tasks',
      component: Dashboard,
      meta: {
        auth: true
      }
    },

    {
      path: '/tasks/:id',
      name: 'task-detail',
      component: TaskDetail,
      meta: {
        auth: true
      }
    }
  ]
})

router.beforeEach((to) => {
  const authenticated =
    !!localStorage.getItem('access_token')

  if (
    to.meta.auth &&
    !authenticated
  ) {
    return '/login'
  }

  if (
    to.path === '/login' &&
    authenticated
  ) {
    return '/tasks'
  }
})

export default router
