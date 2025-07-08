<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTodoStore } from '@/stores/todo'
import type { TodoCreate, CategoryCreate } from '@/interfaces/todolist'

const todoStore = useTodoStore()

// Form states
const todoForm = ref<TodoCreate>({
  title: '',
  description: '',
  completed: false,
  categories: [],
})

const categoryForm = ref<CategoryCreate>({
  name: '',
  description: '',
})

const showAddTodoDialog = ref(false)
const showAddCategoryDialog = ref(false)
const editingTodo = ref<number | null>(null)
const editingCategory = ref<number | null>(null)

// Filter state
const filter = ref<'all' | 'pending' | 'completed'>('all')

// Computed
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

const categoryOptions = computed(() =>
  todoStore.categories.map((cat) => ({
    label: cat.name,
    value: cat.id,
  })),
)

// Methods
const resetTodoForm = () => {
  todoForm.value = {
    title: '',
    description: '',
    completed: false,
    categories: [],
  }
  editingTodo.value = null
}

const resetCategoryForm = () => {
  categoryForm.value = {
    name: '',
    description: '',
  }
  editingCategory.value = null
}

const handleAddTodo = async () => {
  try {
    if (editingTodo.value) {
      await todoStore.updateTodo(editingTodo.value, todoForm.value)
    } else {
      await todoStore.addTodo(todoForm.value)
    }
    showAddTodoDialog.value = false
    resetTodoForm()
  } catch {
    // Error is handled in the store
  }
}

const handleEditTodo = (todoId: number) => {
  const todo = todoStore.todos.find((t) => t.id === todoId)
  if (todo) {
    todoForm.value = {
      title: todo.title,
      description: todo.description || '',
      completed: todo.completed,
      categories: todo.categories.map((cat) => cat.id),
    }
    editingTodo.value = todoId
    showAddTodoDialog.value = true
  }
}

const handleDeleteTodo = async (todoId: number) => {
  if (confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
    await todoStore.removeTodo(todoId)
  }
}

const handleAddCategory = async () => {
  try {
    if (editingCategory.value) {
      await todoStore.updateCategory(editingCategory.value, categoryForm.value)
    } else {
      await todoStore.addCategory(categoryForm.value)
    }
    showAddCategoryDialog.value = false
    resetCategoryForm()
  } catch {
    // Error is handled in the store
  }
}

const handleEditCategory = (categoryId: number) => {
  const category = todoStore.categories.find((c) => c.id === categoryId)
  if (category) {
    categoryForm.value = {
      name: category.name,
      description: category.description || '',
    }
    editingCategory.value = categoryId
    showAddCategoryDialog.value = true
  }
}

const handleDeleteCategory = async (categoryId: number) => {
  if (confirm('¿Estás seguro de que quieres eliminar esta categoría?')) {
    await todoStore.removeCategory(categoryId)
  }
}

onMounted(async () => {
  await Promise.all([todoStore.fetchTodos(), todoStore.fetchCategories()])
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
          @click="showAddTodoDialog = true"
          class="bg-blue-600 hover:bg-blue-700 border-blue-600 hover:border-blue-700"
        />
      </div>
    </div>

    <!-- Error Message -->
    <PMessage
      v-if="todoStore.error"
      severity="error"
      :closable="true"
      @close="todoStore.clearError"
      class="rounded-lg"
    >
      {{ todoStore.error }}
    </PMessage>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Total de tareas</p>
            <p class="text-2xl font-bold text-gray-900">{{ todoStore.todos.length }}</p>
          </div>
          <div class="p-3 bg-blue-100 rounded-lg">
            <i class="pi pi-list text-blue-600 text-xl"></i>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Pendientes</p>
            <p class="text-2xl font-bold text-amber-600">{{ todoStore.pendingTodos.length }}</p>
          </div>
          <div class="p-3 bg-amber-100 rounded-lg">
            <i class="pi pi-clock text-amber-600 text-xl"></i>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Completadas</p>
            <p class="text-2xl font-bold text-green-600">{{ todoStore.completedTodos.length }}</p>
          </div>
          <div class="p-3 bg-green-100 rounded-lg">
            <i class="pi pi-check-circle text-green-600 text-xl"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter Buttons -->
    <div class="flex flex-wrap gap-2">
      <PButton
        label="Todas"
        :severity="filter === 'all' ? 'primary' : 'secondary'"
        size="small"
        @click="filter = 'all'"
        :class="
          filter === 'all'
            ? 'bg-blue-600 border-blue-600'
            : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
        "
      />
      <PButton
        label="Pendientes"
        :severity="filter === 'pending' ? 'primary' : 'secondary'"
        size="small"
        @click="filter = 'pending'"
        :class="
          filter === 'pending'
            ? 'bg-blue-600 border-blue-600'
            : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
        "
      />
      <PButton
        label="Completadas"
        :severity="filter === 'completed' ? 'primary' : 'secondary'"
        size="small"
        @click="filter = 'completed'"
        :class="
          filter === 'completed'
            ? 'bg-blue-600 border-blue-600'
            : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
        "
      />
    </div>

    <!-- Categories Section -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <i class="pi pi-tags text-blue-600"></i>
        Categorías
      </h2>
      <div class="flex flex-wrap gap-2">
        <PChip
          v-for="category in todoStore.categories"
          :key="category.id"
          :label="category.name"
          class="cursor-pointer bg-blue-100 text-blue-800 hover:bg-blue-200 transition-colors"
          removable
          @remove="handleDeleteCategory(category.id)"
          @click="handleEditCategory(category.id)"
        />
        <div v-if="todoStore.categories.length === 0" class="text-gray-500 text-sm py-2">
          No hay categorías creadas. ¡Crea tu primera categoría!
        </div>
      </div>
    </div>

    <!-- Loading Spinner -->
    <div v-if="todoStore.loading" class="flex justify-center items-center py-12">
      <PProgressSpinner class="w-8 h-8" />
      <span class="ml-3 text-gray-600">Cargando tareas...</span>
    </div>

    <!-- Todo List -->
    <div v-else class="space-y-4">
      <div
        v-for="todo in filteredTodos"
        :key="todo.id"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-3">
              <PCheckbox
                :model-value="todo.completed"
                @update:model-value="todoStore.toggleTodoComplete(todo.id)"
                class="scale-110"
              />
              <h3
                class="text-lg font-semibold text-gray-900 flex-1"
                :class="{ 'line-through text-gray-500': todo.completed }"
              >
                {{ todo.title }}
              </h3>
              <span
                :class="
                  todo.completed
                    ? 'bg-green-100 text-green-800 border border-green-200'
                    : 'bg-amber-100 text-amber-800 border border-amber-200'
                "
                class="px-3 py-1 rounded-full text-xs font-medium"
              >
                {{ todo.completed ? 'Completada' : 'Pendiente' }}
              </span>
            </div>

            <p
              v-if="todo.description"
              class="text-gray-600 mb-3"
              :class="{ 'line-through text-gray-400': todo.completed }"
            >
              {{ todo.description }}
            </p>

            <div v-if="todo.categories.length > 0" class="flex flex-wrap gap-2">
              <span
                v-for="category in todo.categories"
                :key="category.id"
                class="bg-blue-50 text-blue-700 px-2 py-1 rounded-md text-xs font-medium border border-blue-200"
              >
                {{ category.name }}
              </span>
            </div>
          </div>

          <div class="flex gap-2 ml-4">
            <PButton
              icon="pi pi-pencil"
              severity="secondary"
              size="small"
              @click="handleEditTodo(todo.id)"
              class="bg-gray-100 hover:bg-gray-200 text-gray-700 border-gray-300"
            />
            <PButton
              icon="pi pi-trash"
              severity="danger"
              size="small"
              @click="handleDeleteTodo(todo.id)"
              class="bg-red-100 hover:bg-red-200 text-red-700 border-red-300"
            />
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-if="filteredTodos.length === 0"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center"
      >
        <div class="max-w-sm mx-auto">
          <i class="pi pi-inbox text-gray-400 text-5xl mb-4"></i>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">
            No hay tareas
            {{ filter === 'all' ? '' : filter === 'pending' ? 'pendientes' : 'completadas' }}
          </h3>
          <p class="text-gray-600 mb-6">
            {{
              filter === 'all'
                ? '¡Comienza creando tu primera tarea!'
                : filter === 'pending'
                  ? 'Todas las tareas están completadas. ¡Buen trabajo!'
                  : 'No hay tareas completadas aún.'
            }}
          </p>
          <PButton
            v-if="filter === 'all'"
            icon="pi pi-plus"
            label="Crear Primera Tarea"
            @click="showAddTodoDialog = true"
            class="bg-blue-600 hover:bg-blue-700 border-blue-600"
          />
        </div>
      </div>
    </div>

    <!-- Add/Edit Todo Dialog -->
    <PDialog
      v-model:visible="showAddTodoDialog"
      :header="editingTodo ? 'Editar Tarea' : 'Nueva Tarea'"
      modal
      class="w-full max-w-md"
      @hide="resetTodoForm"
    >
      <div class="flex flex-col gap-4">
        <div>
          <label for="title" class="block text-sm font-medium mb-2">Título *</label>
          <PInputText id="title" v-model="todoForm.title" class="w-full" required />
        </div>

        <div>
          <label for="description" class="block text-sm font-medium mb-2">Descripción</label>
          <PTextarea id="description" v-model="todoForm.description" class="w-full" rows="3" />
        </div>

        <div>
          <label for="categories" class="block text-sm font-medium mb-2">Categorías</label>
          <PMultiSelect
            id="categories"
            v-model="todoForm.categories"
            :options="categoryOptions"
            option-label="label"
            option-value="value"
            placeholder="Seleccionar categorías"
            class="w-full"
          />
        </div>

        <div class="flex align-items-center gap-2">
          <PCheckbox id="completed" v-model="todoForm.completed" />
          <label for="completed" class="text-sm font-medium">Completada</label>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <PButton label="Cancelar" severity="secondary" @click="showAddTodoDialog = false" />
          <PButton
            :label="editingTodo ? 'Actualizar' : 'Crear'"
            :disabled="!todoForm.title.trim()"
            @click="handleAddTodo"
          />
        </div>
      </template>
    </PDialog>

    <!-- Add/Edit Category Dialog -->
    <PDialog
      v-model:visible="showAddCategoryDialog"
      :header="editingCategory ? 'Editar Categoría' : 'Nueva Categoría'"
      modal
      class="w-full max-w-md"
      @hide="resetCategoryForm"
    >
      <div class="flex flex-col gap-4">
        <div>
          <label for="categoryName" class="block text-sm font-medium mb-2">Nombre *</label>
          <PInputText id="categoryName" v-model="categoryForm.name" class="w-full" required />
        </div>

        <div>
          <label for="categoryDescription" class="block text-sm font-medium mb-2"
            >Descripción</label
          >
          <PTextarea
            id="categoryDescription"
            v-model="categoryForm.description"
            class="w-full"
            rows="3"
          />
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <PButton label="Cancelar" severity="secondary" @click="showAddCategoryDialog = false" />
          <PButton
            :label="editingCategory ? 'Actualizar' : 'Crear'"
            :disabled="!categoryForm.name.trim()"
            @click="handleAddCategory"
          />
        </div>
      </template>
    </PDialog>
  </div>
</template>

<style scoped>
.line-through {
  text-decoration: line-through;
}
</style>
