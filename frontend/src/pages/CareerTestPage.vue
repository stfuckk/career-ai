<template>
  <div class="flex min-h-screen items-center justify-center bg-[#171454] px-4 text-center text-white">
    <RouterLink to="/auth" class="rounded-full bg-white/10 px-6 py-3 text-sm font-semibold uppercase tracking-[0.14em] backdrop-blur-md transition hover:bg-white/15">
      Перейти к авторизации и тесту
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
