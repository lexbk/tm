import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import {
  taskApi,
  type TaskFilters,
  type TaskPayload
} from '../api/tasks'

import type {
  Task,
  TaskPriority,
  TaskStatus
} from '../types/api'

export const useTaskStore = defineStore(
  'tasks',
  () => {
    const tasks = ref<Task[]>([])
    const total = ref(0)
    const loading = ref(false)
    const error = ref('')

    const filters = ref<TaskFilters>({
      limit: 50,
      offset: 0
    })

    const stats = computed(() => ({
      all: total.value,

      todo: tasks.value.filter(
        (task) => task.status === 'TODO'
      ).length,

      progress: tasks.value.filter(
        (task) => task.status === 'IN_PROGRESS'
      ).length,

      done: tasks.value.filter(
        (task) => task.status === 'DONE'
      ).length
    }))

    async function fetchTasks(
      nextFilters: TaskFilters = {}
    ) {
      loading.value = true
      error.value = ''

      try {
        filters.value = {
          ...filters.value,
          ...nextFilters
        }

        const { data } =
          await taskApi.list(filters.value)

        tasks.value = data.results
        total.value = data.count
      } catch (err) {
        error.value =
          'Unable to load tasks.'
        throw err
      } finally {
        loading.value = false
      }
    }

    async function create(
      payload: TaskPayload
    ) {
      const { data } =
        await taskApi.create(payload)

      tasks.value.unshift(data)
      total.value += 1

      return data
    }

    async function update(
      id: string,
      payload: Partial<TaskPayload>
    ) {
      const { data } =
        await taskApi.update(id, payload)

      const index =
        tasks.value.findIndex(
          (task) => task.id === id
        )

      if (index !== -1) {
        tasks.value[index] = {
          ...tasks.value[index],
          ...data
        }
      }

      return data
    }

    async function remove(id: string) {
      await taskApi.remove(id)

      tasks.value =
        tasks.value.filter(
          (task) => task.id !== id
        )

      total.value -= 1
    }

    return {
      tasks,
      total,
      loading,
      error,
      filters,
      stats,
      fetchTasks,
      create,
      update,
      remove
    }
  }
)
