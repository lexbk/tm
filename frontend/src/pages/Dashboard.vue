<script setup lang="ts">
import {
  computed,
  onMounted,
  ref
} from 'vue'

import { useRouter } from 'vue-router'
import {
  useTaskStore
} from '../stores/tasks'

import type {
  Task,
  TaskPriority,
  TaskStatus
} from '../types/api'

import TaskCard
  from '../components/TaskCard.vue'

import TaskModal
  from '../components/TaskModal.vue'

const store = useTaskStore()
const router = useRouter()

const query = ref('')
const status =
  ref<TaskStatus | ''>('')
const priority =
  ref<TaskPriority | ''>('')

const modal = ref(false)
const editing = ref<Task | null>(null)

const filtered = computed(() =>
  store.tasks.filter((task) =>
    task.title
      .toLowerCase()
      .includes(
        query.value.toLowerCase()
      )
  )
)

onMounted(() => {
  store.fetchTasks()
})

function openCreate() {
  editing.value = null
  modal.value = true
}

function openTask(task: Task) {
  router.push(`/tasks/${task.id}`)
}

function openEdit(task: Task) {
  editing.value = task
  modal.value = true
}

async function save(payload: any) {
  try {
    if (editing.value) {
      await store.update(
        editing.value.id,
        payload
      )
    } else {
      await store.create(payload)
    }

    modal.value = false
  } catch {
    // API errors are handled by the store.
  }
}

async function remove(task: Task) {
  if (
    confirm(
      `Delete "${task.title}"?`
    )
  ) {
    await store.remove(task.id)
  }
}

async function apply() {
  await store.fetchTasks({
    status: status.value,
    priority: priority.value,
    offset: 0
  })
}
</script>

<template>
  <header class="page-header">
    <div>
      <span class="eyebrow">
        Workspace
      </span>

      <h1>Tasks</h1>

      <p>
        Plan, prioritize, and keep work moving.
      </p>
    </div>

    <button
      class="btn primary"
      @click="openCreate"
    >
      + New task
    </button>
  </header>

  <section class="stats">
    <div>
      <span>All tasks</span>
      <strong>
        {{ store.stats.all }}
      </strong>
    </div>

    <div>
      <span>To do</span>
      <strong>
        {{ store.stats.todo }}
      </strong>
    </div>

    <div>
      <span>In progress</span>
      <strong>
        {{ store.stats.progress }}
      </strong>
    </div>

    <div>
      <span>Completed</span>
      <strong>
        {{ store.stats.done }}
      </strong>
    </div>
  </section>

  <section class="toolbar">
    <div class="search">
      <span>⌕</span>

      <input
        v-model="query"
        placeholder="Search tasks..."
      />
    </div>

    <select
      v-model="status"
      @change="apply"
    >
      <option value="">
        All statuses
      </option>

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

    <select
      v-model="priority"
      @change="apply"
    >
      <option value="">
        All priorities
      </option>

      <option value="LOW">
        Low
      </option>

      <option value="MEDIUM">
        Medium
      </option>

      <option value="HIGH">
        High
      </option>

      <option value="URGENT">
        Urgent
      </option>
    </select>
  </section>

  <div
    v-if="store.loading"
    class="state"
  >
    Loading tasks...
  </div>

  <div
    v-else-if="store.error"
    class="state error"
  >
    {{ store.error }}
  </div>

  <div
    v-else-if="!filtered.length"
    class="empty"
  >
    <div class="empty-icon">
      ✓
    </div>

    <h2>
      No tasks found
    </h2>

    <p>
      Create a task or change your filters.
    </p>

    <button
      class="btn primary"
      @click="openCreate"
    >
      Create task
    </button>
  </div>

  <section
    v-else
    class="task-grid"
  >
    <TaskCard
      v-for="task in filtered"
      :key="task.id"
      :task="task"
      @open="openTask"
      @edit="openEdit"
      @remove="remove"
    />
  </section>

  <TaskModal
    :open="modal"
    :task="editing"
    @close="modal = false"
    @save="save"
  />
</template>
