<template>
  <header class="px-0 sm:px-20 lg:px-25">
    <div class="rounded-b-4xl bg-white/96 shadow-[0_14px_40px_rgba(29,16,126,0.08)]">
    <div
      class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-10"
    >
      <a
        class="text-sm font-semibold tracking-[0.02em] text-[#0E005D]! transition hover:opacity-80"
        href="#"
      >
        Поиск вакансий
      </a>

      <RouterLink
        to="/"
        class="flex h-11 min-w-20 items-center justify-center rounded-full bg-[#0E005D] px-8 text-sm font-semibold uppercase tracking-[0.18em] text-white! shadow-[0_10px_30px_rgba(29,16,126,0.24)] transition hover:scale-[1.01]"
        style="color: #fff"
      >
        Лого
      </RouterLink>

      <div class="flex items-center gap-2 text-[#1d107e] sm:gap-3">
        <RouterLink
          to="/auth"
          class="flex h-10 w-10 items-center justify-center rounded-full transition hover:bg-[#1d107e]/5"
          aria-label="Авторизация"
        >
          <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21a8 8 0 0 0-16 0" />
            <circle cx="12" cy="8" r="4" />
          </svg>
        </RouterLink>

        <button
          type="button"
          class="flex h-10 w-10 items-center justify-center rounded-full transition hover:bg-[#1d107e]/5"
          aria-label="Сменить тему"
        >
          <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8Z" />
          </svg>
        </button>
      </div>
    </div>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
