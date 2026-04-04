<template>
  <header class="relative z-30 shrink-0 px-0 sm:px-20 lg:px-25">
    <div class="rounded-b-4xl bg-(--surface) shadow-(--shadow-header) transition-colors duration-300">
      <div
        class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-10"
      >
        <RouterLink
          to="/vacancies"
          class="text-sm font-semibold tracking-[0.02em] text-(--text-hero) transition hover:opacity-80"
        >
          Поиск вакансий
        </RouterLink>

        <RouterLink
          to="/"
          class="flex h-11 min-w-20 items-center justify-center rounded-full bg-(--button-primary) px-8 text-sm font-semibold uppercase tracking-[0.18em] text-(--button-text) shadow-[0_10px_30px_rgba(29,16,126,0.24)] transition hover:scale-[1.01] hover:bg-(--button-primary-hover)"
          style="color: var(--button-text)"
        >
          Лого
        </RouterLink>

        <div class="flex items-center gap-2 text-(--text-hero) sm:gap-3">
          <RouterLink
            to="/auth"
            class="flex h-10 w-10 items-center justify-center rounded-full transition hover:bg-(--surface-soft-2)"
            aria-label="Авторизация"
          >
            <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21a8 8 0 0 0-16 0" />
              <circle cx="12" cy="8" r="4" />
            </svg>
          </RouterLink>

          <button
            type="button"
            class="flex h-10 w-10 items-center justify-center rounded-full transition hover:bg-(--surface-soft-2)"
            aria-label="Сменить тему"
            @click="toggleTheme"
          >
            <svg
              v-if="isDark"
              viewBox="0 0 24 24"
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="12" r="4" />
              <path d="M12 2v2" />
              <path d="M12 20v2" />
              <path d="m4.93 4.93 1.41 1.41" />
              <path d="m17.66 17.66 1.41 1.41" />
              <path d="M2 12h2" />
              <path d="M20 12h2" />
              <path d="m6.34 17.66-1.41 1.41" />
              <path d="m19.07 4.93-1.41 1.41" />
            </svg>
            <svg v-else viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
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

import { useTheme } from '@/composables/useTheme'

const { isDark, toggleTheme } = useTheme()
</script>
