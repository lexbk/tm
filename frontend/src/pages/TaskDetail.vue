<script setup lang="ts">
import {
  onMounted,
  ref,
  watch
} from 'vue'

import {
  useRoute,
  useRouter
} from 'vue-router'

import TaskModal from '../components/TaskModal.vue'

import { taskApi } from '../api/tasks'
import type {
  Comment,
  Task
} from '../types/api'

const route = useRoute()
const router = useRouter()

const task = ref<Task | null>(null)
const comments = ref<Comment[]>([])
const commentBody = ref('')

const loading = ref(true)
const submitting = ref(false)
const error = ref('')

const updateError = ref('')

const modalOpen = ref(false)

watch(
  () => modalOpen.value,
  (open) => {
    if (!open) updateError.value = ''
  }
)

const taskId = route.params.id as string

async function load() {
  loading.value = true
  error.value = ''

  try {
    const [
      taskResponse,
      commentsResponse
    ] = await Promise.all([
      taskApi.get(taskId),
      taskApi.comments(taskId)
    ])

    task.value = taskResponse.data
    comments.value =
      commentsResponse.data.results
  } catch {
    error.value =
      'Unable to load the task.'
  } finally {
    loading.value = false
  }
}

async function addComment() {
  const body =
    commentBody.value.trim()

  if (!body) return

  submitting.value = true

  try {
    const { data } =
      await taskApi.addComment(
        taskId,
        body
      )

    comments.value.push(data)
    commentBody.value = ''
  } catch {
    error.value =
      'Unable to add comment.'
  } finally {
    submitting.value = false
  }
}

async function deleteComment(
  comment: Comment
) {
  if (
    !confirm(
      'Delete this comment?'
    )
  ) {
    return
  }

  await taskApi.removeComment(
    taskId,
    comment.id
  )

  comments.value =
    comments.value.filter(
      (item) =>
        item.id !== comment.id
    )
}

async function deleteTask() {
  if (!task.value) return

  if (
    !confirm(
      `Delete "${task.value.title}"?`
    )
  ) {
    return
  }

  await taskApi.remove(taskId)

  router.push('/tasks')
}

async function save(payload: any) {
  if (!task.value) return

  submitting.value = true

  try {
    const { data } = await taskApi.update(
      taskId,
      payload
    )

    task.value = data
  } catch {
    updateError.value = 'Unable to update task.'
  } finally {
    submitting.value = false
    modalOpen.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="detail">
    <button
      class="back"
      @click="router.push('/tasks')"
    >
      ← Back to tasks
    </button>

    <div
      v-if="loading"
      class="state"
    >
      Loading task...
    </div>

    <div
      v-else-if="error"
      class="state error"
    >
      {{ error }}
    </div>

    <div
      v-else-if="task"
      class="detail-layout"
    >
      <div
        v-if="updateError"
        class="state error"
      >
        {{ updateError }}
      </div>

      <article class="detail-main">
        <div class="detail-title">
          <span
            :class="[
              'status-dot',
              task.status.toLowerCase()
            ]"
          />

          <span
            :class="[
              'status-text',
              task.status.toLowerCase()
            ]"
          >
            {{
              task.status === 'IN_PROGRESS'
                ? 'In progress'
                : task.status === 'TODO'
                  ? 'To do'
                  : 'Done'
            }}
          </span>
        </div>

        <h1>
          {{ task.title }}
        </h1>

        <p class="description">
          {{
            task.description ||
            'No description provided.'
          }}
        </p>

        <div class="detail-actions">
          <button
            class="btn primary"
            @click="modalOpen = true"
          >
            Edit task
          </button>

          <button
            class="btn danger"
            @click="deleteTask"
          >
            Delete task
          </button>
        </div>

        <hr />

        <h2>
          Comments
          <span>
            {{ comments.length }}
          </span>
        </h2>

        <div class="comment-compose">
          <textarea
            v-model="commentBody"
            rows="3"
            maxlength="10000"
            placeholder="Write a comment..."
          />

          <button
            class="btn primary"
            :disabled="submitting"
            @click="addComment"
          >
            {{
              submitting
                ? 'Posting...'
                : 'Add comment'
            }}
          </button>
        </div>

        <div
          v-if="!comments.length"
          class="state"
        >
          No comments yet.
        </div>

        <div
          v-for="comment in comments"
          :key="comment.id"
          class="comment"
        >
          <span class="avatar small">
            {{
              comment.author.username
                .charAt(0)
                .toUpperCase()
            }}
          </span>

          <div>
            <b>
              {{ comment.author.username }}
            </b>

            <small>
              {{
                new Date(
                  comment.created_at
                ).toLocaleString()
              }}
            </small>

            <p>
              {{ comment.body }}
            </p>

            <button
              class="icon-btn"
              @click="deleteComment(comment)"
            >
              Delete
            </button>
          </div>
        </div>
      </article>

      <aside class="detail-side">
        <div>
          <span>Priority</span>

          <strong>
            {{ task.priority }}
          </strong>
        </div>

        <div>
          <span>Assignee</span>

          <strong>
            {{
              task.assignee?.username ||
              'Unassigned'
            }}
          </strong>
        </div>

        <div>
          <span>Creator</span>

          <strong>
            {{
              task.creator?.username ||
              'Unknown'
            }}
          </strong>
        </div>

        <div>
          <span>Due date</span>

          <strong>
            {{
              task.due_date
                ? new Date(
                    task.due_date
                  ).toLocaleString()
                : 'No due date'
            }}
          </strong>
        </div>

        <div>
          <span>Created</span>

          <strong>
            {{
              task.created_at
                ? new Date(
                    task.created_at
                  ).toLocaleString()
                : '—'
            }}
          </strong>
        </div>
      </aside>
    </div>
  </div>

  <TaskModal
    :open="modalOpen"
    :task="task"
    @close="modalOpen = false"
    @save="save"
  />
</template>
