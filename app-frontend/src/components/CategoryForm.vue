<script setup lang="ts">
import { ref, watch } from 'vue'
import { useCategoryStore } from '@/stores/category'
import type { CategoryCreate } from '@/interfaces/todolist'

interface Props {
  visible: boolean
  editingCategoryId?: number | null
}

interface Emits {
  (e: 'update:visible', value: boolean): void
  (e: 'category-saved'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const categoryStore = useCategoryStore()

const categoryForm = ref<CategoryCreate>({
  name: '',
  description: '',
})

const resetForm = () => {
  categoryForm.value = {
    name: '',
    description: '',
  }
}

const handleSubmit = async () => {
  try {
    if (props.editingCategoryId) {
      await categoryStore.updateCategory(props.editingCategoryId, categoryForm.value)
    } else {
      await categoryStore.addCategory(categoryForm.value)
    }
    emit('update:visible', false)
    emit('category-saved')
    resetForm()
  } catch {
    // Error is handled in the store
  }
}

const handleCancel = () => {
  emit('update:visible', false)
  resetForm()
}

// Load category data when editing
watch(
  () => props.editingCategoryId,
  (categoryId) => {
    if (categoryId) {
      const category = categoryStore.categories.find((c) => c.id === categoryId)
      if (category) {
        categoryForm.value = {
          name: category.name,
          description: category.description || '',
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
    :header="editingCategoryId ? 'Editar Categoría' : 'Nueva Categoría'"
    modal
    class="w-full max-w-md"
    @update:visible="emit('update:visible', $event)"
    @hide="resetForm"
  >
    <div class="flex flex-col gap-4">
      <div>
        <label for="categoryName" class="block text-sm font-medium mb-2">Nombre *</label>
        <PInputText id="categoryName" v-model="categoryForm.name" class="w-full" required />
      </div>

      <div>
        <label for="categoryDescription" class="block text-sm font-medium mb-2">Descripción</label>
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
        <PButton label="Cancelar" severity="secondary" @click="handleCancel" />
        <PButton
          :label="editingCategoryId ? 'Actualizar' : 'Crear'"
          :disabled="!categoryForm.name.trim()"
          @click="handleSubmit"
        />
      </div>
    </template>
  </PDialog>
</template>
