<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTodoStore } from '@/stores/todos'
import { useCategoryStore } from '@/stores/category'
import TodoStatsCards from './TodoStatsCards.vue'
import TodoFilters from './TodoFilters.vue'
import CategorySection from './CategorySection.vue'
import TodoItem from './TodoItem.vue'
import TodoForm from './TodoForm.vue'
import CategoryForm from './CategoryForm.vue'
import EmptyState from './EmptyState.vue'

const todoStore = useTodoStore()
const categoryStore = useCategoryStore()

// Dialog states
const showAddTodoDialog = ref(false)
const showAddCategoryDialog = ref(false)
const editingTodo = ref<number | null>(null)
const editingCategory = ref<number | null>(null)

// Filter state
const filter = ref<'all' | 'pending' | 'completed'>('all')

// Computed - check for errors in both stores
const hasError = computed(() => todoStore.error || categoryStore.error)
const currentError = computed(() => todoStore.error || categoryStore.error)
const isLoading = computed(() => todoStore.loading || categoryStore.loading)

const filteredTodos = computed(() => {
  switch (filter.value) {
    case 'pending':
      return todoStore.pendingTodos
    case 'completed':
      return todoStore.completedTodos
    default:
      return todoStore.todos
  }
})

// Methods
const clearAllErrors = () => {
  todoStore.clearError()
  categoryStore.clearError()
}

const handleEditTodo = (todoId: number) => {
  editingTodo.value = todoId
  showAddTodoDialog.value = true
}

const handleEditCategory = (categoryId: number) => {
  editingCategory.value = categoryId
  showAddCategoryDialog.value = true
}

const handleTodoSaved = () => {
  editingTodo.value = null
}

const handleCategorySaved = () => {
  editingCategory.value = null
}

const handleCreateTodo = () => {
  editingTodo.value = null
  showAddTodoDialog.value = true
}

onMounted(async () => {
  await Promise.all([todoStore.fetchTodos(), categoryStore.fetchCategories()])
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Lista de Tareas</h1>
        <p class="text-gray-600 mt-1">Organiza y gestiona tus tareas diarias</p>
      </div>
      <div class="flex gap-3">
        <PButton
          icon="pi pi-plus"
          label="Nueva Categoría"
          severity="secondary"
          size="small"
          @click="showAddCategoryDialog = true"
          class="bg-white border border-gray-300 hover:bg-gray-50 text-gray-700"
        />
        <PButton
          icon="pi pi-plus"
          label="Nueva Tarea"
          size="small"
          @click="handleCreateTodo"
          class="bg-blue-600 hover:bg-blue-700 border-blue-600 hover:border-blue-700"
        />
      </div>
    </div>

    <!-- Error Message -->
    <PMessage
      v-if="hasError"
      severity="error"
      :closable="true"
      @close="clearAllErrors"
      class="rounded-lg"
    >
      {{ currentError }}
    </PMessage>

    <!-- Stats Cards -->
    <TodoStatsCards />

    <!-- Filter Buttons -->
    <TodoFilters v-model="filter" />

    <!-- Categories Section -->
    <CategorySection @edit-category="handleEditCategory" />

    <!-- Loading Spinner -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <PProgressSpinner class="w-8 h-8" />
      <span class="ml-3 text-gray-600">Cargando...</span>
    </div>

    <!-- Todo List -->
    <div v-else class="space-y-4">
      <TodoItem
        v-for="todo in filteredTodos"
        :key="todo.id"
        :todo="todo"
        @edit-todo="handleEditTodo"
      />

      <!-- Empty State -->
      <EmptyState
        v-if="filteredTodos.length === 0"
        :filter="filter"
        @create-todo="handleCreateTodo"
      />
    </div>

    <!-- Todo Form Dialog -->
    <TodoForm
      v-model:visible="showAddTodoDialog"
      :editing-todo-id="editingTodo"
      @todo-saved="handleTodoSaved"
    />

    <!-- Category Form Dialog -->
    <CategoryForm
      v-model:visible="showAddCategoryDialog"
      :editing-category-id="editingCategory"
      @category-saved="handleCategorySaved"
    />
  </div>
</template>
