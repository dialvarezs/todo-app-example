<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const items = [{ label: 'Inicio', command: () => router.push({ name: 'home' }) }]
</script>

<template>
  <Menubar :model="items">
    <template #end>
      <span class="mr-2">Hola, user</span>
      <Button>Cerrar Sesión</Button>
    </template>
  </Menubar>
</template>
