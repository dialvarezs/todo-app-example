<script setup lang="ts">
import BaseHeader from '@/components/base/BaseHeader.vue'
</script>

<template>
  <template class="container mx-auto my-2">
    <BaseHeader class="mb-3 !bg-gray-100" />
    <RouterView />
  </template>
</template>

<style scoped></style>
