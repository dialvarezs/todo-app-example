<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useTodoStore } from '@/stores/todos'
import { useCategoryStore } from '@/stores/category'
import type { TodoCreate } from '@/interfaces/todolist'

interface Props {
  visible: boolean
  editingTodoId?: number | null
}

interface Emits {
  (e: 'update:visible', value: boolean): void
  (e: 'todo-saved'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const todoStore = useTodoStore()
const categoryStore = useCategoryStore()

const todoForm = ref<TodoCreate>({
  title: '',
  description: '',
  completed: false,
  categories: [],
})

const categoryOptions = computed(() =>
  categoryStore.categories.map((cat) => ({
    label: cat.name,
    value: cat.id,
  })),
)

const resetForm = () => {
  todoForm.value = {
    title: '',
    description: '',
    completed: false,
    categories: [],
  }
}

const handleSubmit = async () => {
  try {
    if (props.editingTodoId) {
      await todoStore.updateTodo(props.editingTodoId, todoForm.value)
    } else {
      await todoStore.addTodo(todoForm.value)
    }
    emit('update:visible', false)
    emit('todo-saved')
    resetForm()
  } catch {
    // Error is handled in the store
  }
}

const handleCancel = () => {
  emit('update:visible', false)
  resetForm()
}

// Load todo data when editing
watch(
  () => props.editingTodoId,
  (todoId) => {
    if (todoId) {
      const todo = todoStore.todos.find((t) => t.id === todoId)
      if (todo) {
        todoForm.value = {
          title: todo.title,
          description: todo.description || '',
          completed: todo.completed,
          categories: todo.categories.map((cat) => cat.id),
        }
      }
    } else {
      resetForm()
    }
  },
  { immediate: true },
)
</script>

<template>
  <PDialog
    :visible="visible"
    :header="editingTodoId ? 'Editar Tarea' : 'Nueva Tarea'"
    modal
    class="w-full max-w-md"
    @update:visible="emit('update:visible', $event)"
    @hide="resetForm"
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
        <PButton label="Cancelar" severity="secondary" @click="handleCancel" />
        <PButton
          :label="editingTodoId ? 'Actualizar' : 'Crear'"
          :disabled="!todoForm.title.trim()"
          @click="handleSubmit"
        />
      </div>
    </template>
  </PDialog>
</template>
