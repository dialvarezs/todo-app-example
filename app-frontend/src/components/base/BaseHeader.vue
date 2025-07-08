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
            <i class="pi pi-check text-white font-bold"></i>
          </div>
          <h1 class="text-xl font-bold text-gray-900">TodoApp</h1>
        </div>

        <nav class="hidden md:flex space-x-1">
          <a
            v-for="item in items"
            :key="item.label"
            href="#"
            @click.prevent="item.command?.()"
            class="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
          >
            <i :class="item.icon" class="mr-2"></i>
            {{ item.label }}
          </a>
        </nav>
      </div>

      <div class="flex items-center space-x-4">
        <span class="text-sm text-gray-600 hidden sm:block">Hola, usuario</span>
        <PButton
          icon="pi pi-sign-out"
          label="Cerrar Sesión"
          severity="secondary"
          size="small"
          class="bg-gray-100 hover:bg-gray-200 text-gray-700 border-gray-300"
        />
      </div>
    </div>
  </nav>
</template>
