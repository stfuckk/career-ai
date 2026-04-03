<template>
  <div class="min-h-screen bg-[(--page-bg)] text-[(--text-main)] transition-colors duration-300">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>
