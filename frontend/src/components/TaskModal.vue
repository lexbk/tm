<script setup lang="ts">
import {
  onMounted,
  reactive,
  ref,
  watch
} from 'vue'

import { userApi } from '../api/users'

import type {
  Task,
  TaskPriority,
  TaskStatus,
  UserInfo
} from '../types/api'

const props = defineProps<{
  open: boolean
  task?: Task | null
}>()

const emit = defineEmits<{
  close: []
  save: [payload: any]
}>()

const form = reactive({
  title: '',
  description: '',
  status: 'TODO' as TaskStatus,
  priority: 'MEDIUM' as TaskPriority,
  due_date: '',
  assignee_id: '' as string | ''
})

const users = ref<UserInfo[]>([])
const loadingUsers = ref(false)

async function fetchUsers() {
  loadingUsers.value = true
  try {
    const res = await userApi.list({ limit: 100 })
    users.value = res.data.results
  } catch {
    users.value = []
  } finally {
    loadingUsers.value = false
  }
}

onMounted(fetchUsers)

watch(
  () => props.open,
  (open) => {
    if (!open) return

    Object.assign(form, {
      title: props.task?.title || '',
      description:
        props.task?.description || '',
      status:
        props.task?.status || 'TODO',
      priority:
        props.task?.priority || 'MEDIUM',
      due_date:
        props.task?.due_date
          ? props.task.due_date.slice(0, 16)
          : '',
      assignee_id: props.task?.assignee_id || ''
    })
  }
)

function submit() {
  if (!form.title.trim()) {
    return
  }

  const payload: Record<string, unknown> = {
    title: form.title.trim(),
    description: form.description,
    status: form.status,
    priority: form.priority
  }

  if (form.assignee_id) {
    payload.assignee_id = form.assignee_id
  } else if (props.task?.assignee_id) {
    payload.assignee_id = null
  }

  if (form.due_date) {
    payload.due_date = new Date(
      form.due_date
    ).toISOString()
  } else {
    payload.due_date = null
  }

  emit('save', payload)
}
</script>

<template>
  <div
    v-if="open"
    class="modal-backdrop"
    @click.self="emit('close')"
  >
    <form
      class="modal"
      @submit.prevent="submit"
    >
      <div class="modal-head">
        <div>
          <span class="eyebrow">
            {{
              task
                ? 'Edit task'
                : 'New task'
            }}
          </span>

          <h2>
            {{
              task
                ? 'Update task'
                : 'Create a task'
            }}
          </h2>
        </div>

        <button
          type="button"
          class="close"
          @click="emit('close')"
        >
          ×
        </button>
      </div>

      <label>
        Title

        <input
          v-model="form.title"
          maxlength="255"
          placeholder="e.g. Prepare project brief"
          autofocus
        />
      </label>

      <label>
        Description

        <textarea
          v-model="form.description"
          rows="4"
          placeholder="Add context or notes..."
        />
      </label>

      <div class="form-grid">
        <label>
          Status

          <select v-model="form.status">
            <option value="TODO">
              To do
            </option>

            <option value="IN_PROGRESS">
              In progress
            </option>

            <option value="DONE">
              Done
            </option>
          </select>
        </label>

        <label>
          Priority

          <select v-model="form.priority">
            <option value="LOW">
              LOW
            </option>

            <option value="MEDIUM">
              MEDIUM
            </option>

            <option value="HIGH">
              HIGH
            </option>

            <option value="URGENT">
              URGENT
            </option>
          </select>
        </label>

        <label>
          Assignee

          <select v-model="form.assignee_id">
            <option value="">
              Unassigned
            </option>

            <option
              v-for="user in users"
              :key="user.id"
              :value="user.id"
            >
              {{ user.username }}
            </option>
          </select>
        </label>
      </div>

      <label>
        Due date

        <input
          v-model="form.due_date"
          type="datetime-local"
        />
      </label>

      <div class="modal-actions">
        <button
          type="button"
          class="btn secondary"
          @click="emit('close')"
        >
          Cancel
        </button>

        <button
          class="btn primary"
          type="submit"
        >
          {{
            task
              ? 'Save changes'
              : 'Create task'
          }}
        </button>
      </div>
    </form>
  </div>
</template>
