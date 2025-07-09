<script setup lang="ts">
interface Props {
  modelValue: 'all' | 'pending' | 'completed'
}

interface Emits {
  (e: 'update:modelValue', value: 'all' | 'pending' | 'completed'): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

const updateFilter = (value: 'all' | 'pending' | 'completed') => {
  emit('update:modelValue', value)
}
</script>

<template>
  <div class="flex flex-wrap gap-2">
    <PButton
      label="Todas"
      :severity="modelValue === 'all' ? 'primary' : 'secondary'"
      size="small"
      @click="updateFilter('all')"
      :class="
        modelValue === 'all'
          ? 'bg-blue-600 border-blue-600'
          : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
      "
    />
    <PButton
      label="Pendientes"
      :severity="modelValue === 'pending' ? 'primary' : 'secondary'"
      size="small"
      @click="updateFilter('pending')"
      :class="
        modelValue === 'pending'
          ? 'bg-blue-600 border-blue-600'
          : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
      "
    />
    <PButton
      label="Completadas"
      :severity="modelValue === 'completed' ? 'primary' : 'secondary'"
      size="small"
      @click="updateFilter('completed')"
      :class="
        modelValue === 'completed'
          ? 'bg-blue-600 border-blue-600'
          : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
      "
    />
  </div>
</template>
