<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const items = [
  {
    label: 'Inicio',
    icon: 'pi pi-home',
    command: () => router.push({ name: 'home' }),
  },
]
</script>

<template>
  <nav class="bg-white border-b border-gray-200 px-4 py-3">
    <div class="container mx-auto max-w-7xl flex items-center justify-between">
      <div class="flex items-center space-x-6">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <i class="pi pi-check text-white font-bold" />
          </div>
          <h1 class="text-xl font-bold text-gray-900">
            TodoApp
          </h1>
        </div>

        <nav class="hidden md:flex space-x-1">
          <a
            v-for="item in items"
            :key="item.label"
            href="#"
            class="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
            @click.prevent="item.command?.()"
          >
            <i :class="item.icon" class="mr-2" />
            {{ item.label }}
          </a>
        </nav>
      </div>
    </div>
  </nav>
</template>
