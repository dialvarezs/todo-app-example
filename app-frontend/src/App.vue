<script setup lang="ts">
import BaseHeader from '@/components/base/BaseHeader.vue'
</script>

<template>
  <ConfirmDialog></ConfirmDialog>
  <div class="min-h-screen bg-gray-50">
    <BaseHeader class="shadow-sm bg-white border-b border-gray-200" />
    <main class="container mx-auto px-4 py-8 max-w-7xl">
      <RouterView />
    </main>
  </div>
</template>

<style scoped></style>
