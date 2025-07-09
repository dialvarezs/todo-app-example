<script setup lang="ts">
import { useCategoryStore } from '@/stores/category'

interface Emits {
  (e: 'edit-category', categoryId: number): void
}

const emit = defineEmits<Emits>()
const categoryStore = useCategoryStore()

const handleDeleteCategory = async (categoryId: number) => {
  if (confirm('¿Estás seguro de que quieres eliminar esta categoría?')) {
    await categoryStore.removeCategory(categoryId)
  }
}

const handleEditCategory = (categoryId: number) => {
  emit('edit-category', categoryId)
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
      <i class="pi pi-tags text-blue-600"></i>
      Categorías
    </h2>
    <div class="flex flex-wrap gap-2">
      <PChip
        v-for="category in categoryStore.categories"
        :key="category.id"
        :label="category.name"
        class="cursor-pointer bg-blue-100 text-blue-800 hover:bg-blue-200 transition-colors"
        removable
        @remove="handleDeleteCategory(category.id)"
        @click="handleEditCategory(category.id)"
      />
      <div v-if="categoryStore.categories.length === 0" class="text-gray-500 text-sm py-2">
        No hay categorías creadas. ¡Crea tu primera categoría!
      </div>
    </div>
  </div>
</template>
