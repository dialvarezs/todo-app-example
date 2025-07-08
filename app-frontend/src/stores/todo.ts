import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Todo, TodoCreate, Category, CategoryCreate } from '@/interfaces/todolist'
import * as api from '@/api/todolist'

export const useTodoStore = defineStore('todo', () => {
  // State
  const todos = ref<Todo[]>([])
  const categories = ref<Category[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const completedTodos = computed(() => todos.value.filter((todo) => todo.completed))
  const pendingTodos = computed(() => todos.value.filter((todo) => !todo.completed))

  // Actions
  const setLoading = (value: boolean) => {
    loading.value = value
  }

  const setError = (message: string | null) => {
    error.value = message
  }

  const clearError = () => {
    error.value = null
  }

  // Todo actions
  const fetchTodos = async () => {
    try {
      setLoading(true)
      clearError()
      todos.value = await api.getTodos()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch todos')
    } finally {
      setLoading(false)
    }
  }

  const addTodo = async (todoData: TodoCreate) => {
    try {
      setLoading(true)
      clearError()
      const newTodo = await api.createTodo(todoData)
      todos.value.push(newTodo)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create todo')
      throw err
    } finally {
      setLoading(false)
    }
  }

  const updateTodo = async (id: number, todoData: Partial<TodoCreate>) => {
    try {
      setLoading(true)
      clearError()
      const updatedTodo = await api.updateTodo(id, todoData)
      const index = todos.value.findIndex((todo) => todo.id === id)
      if (index !== -1) {
        todos.value[index] = updatedTodo
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update todo')
      throw err
    } finally {
      setLoading(false)
    }
  }

  const removeTodo = async (id: number) => {
    try {
      setLoading(true)
      clearError()
      await api.deleteTodo(id)
      todos.value = todos.value.filter((todo) => todo.id !== id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete todo')
      throw err
    } finally {
      setLoading(false)
    }
  }

  const toggleTodoComplete = async (id: number) => {
    const todo = todos.value.find((t) => t.id === id)
    if (todo) {
      await updateTodo(id, { completed: !todo.completed })
    }
  }

  // Category actions
  const fetchCategories = async () => {
    try {
      setLoading(true)
      clearError()
      categories.value = await api.getCategories()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch categories')
    } finally {
      setLoading(false)
    }
  }

  const addCategory = async (categoryData: CategoryCreate) => {
    try {
      setLoading(true)
      clearError()
      const newCategory = await api.createCategory(categoryData)
      categories.value.push(newCategory)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create category')
      throw err
    } finally {
      setLoading(false)
    }
  }

  const updateCategory = async (id: number, categoryData: Partial<CategoryCreate>) => {
    try {
      setLoading(true)
      clearError()
      const updatedCategory = await api.updateCategory(id, categoryData)
      const index = categories.value.findIndex((category) => category.id === id)
      if (index !== -1) {
        categories.value[index] = updatedCategory
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update category')
      throw err
    } finally {
      setLoading(false)
    }
  }

  const removeCategory = async (id: number) => {
    try {
      setLoading(true)
      clearError()
      await api.deleteCategory(id)
      categories.value = categories.value.filter((category) => category.id !== id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete category')
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    // State
    todos,
    categories,
    loading,
    error,
    // Computed
    completedTodos,
    pendingTodos,
    // Actions
    clearError,
    fetchTodos,
    addTodo,
    updateTodo,
    removeTodo,
    toggleTodoComplete,
    fetchCategories,
    addCategory,
    updateCategory,
    removeCategory,
  }
})
