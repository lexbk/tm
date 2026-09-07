<script setup lang="ts">
import { ref } from 'vue'

import type { Task } from '../types/api'

defineProps<{
  task: Task
}>()

defineEmits<{
  open: [task: Task]
  edit: [task: Task]
  remove: [task: Task]
}>()

const statusLabel = (status: string) => {
  if (status === 'IN_PROGRESS') {
    return 'In progress'
  }

  if (status === 'TODO') {
    return 'To do'
  }

  return 'Done'
}

const menuOpen = ref(false)
let hideTimer: ReturnType<typeof setTimeout> | null = null

function openMenu() {
  if (hideTimer) {
    clearTimeout(hideTimer)
    hideTimer = null
  }
  menuOpen.value = true
}

function closeMenu() {
  hideTimer = setTimeout(() => {
    menuOpen.value = false
    hideTimer = null
  }, 150)
}
</script>

<template>
  <article
    class="task-card"
    @click="menuOpen = false; $emit('open', task)"
  >
    <div class="card-top">
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
        {{ statusLabel(task.status) }}
      </span>

      <div class="more-wrapper">
        <button
          class="more"
          @mouseenter="openMenu"
          @mouseleave="closeMenu"
        >
          •••
        </button>

        <div
          v-if="menuOpen"
          class="dropdown"
          @mouseenter="openMenu"
          @mouseleave="closeMenu"
        >
          <button
            class="dropdown-item"
            @click.stop="$emit('edit', task)"
          >
            Edit
          </button>

          <button
            class="dropdown-item danger"
            @click.stop="$emit('remove', task)"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    <h3>
      {{ task.title }}
    </h3>

    <p v-if="task.description">
      {{ task.description }}
    </p>

    <div class="card-meta">
      <span
        :class="[
          'priority',
          task.priority.toLowerCase()
        ]"
      >
        {{ task.priority }}
      </span>

      <span v-if="task.due_date">
        Due
        {{
          new Date(
            task.due_date
          ).toLocaleDateString()
        }}
      </span>

      <span v-if="task.assignee">
        @{{ task.assignee.username }}
      </span>
    </div>
  </article>
</template>

<style scoped>
.more-wrapper {
  position: relative;
}

.dropdown {
  position: absolute;
  top: calc(100% + 4px);
  right: 0;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 10;
  min-width: 120px;
  padding: 4px 0;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 8px 16px;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  font: inherit;
  color: inherit;
}

.dropdown-item:hover {
  background: #f3f4f6;
}

.dropdown-item.danger {
  color: #ef4444;
}

.dropdown-item.danger:hover {
  background: #fef2f2;
}
</style>
