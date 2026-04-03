<template>
  <div class="flex min-h-screen flex-col bg-(--page-bg-alt) transition-colors duration-300">
    <SiteHeader />

    <main class="flex-1">
      <section class="px-0 py-10 sm:px-5 sm:py-14 lg:px-32 lg:py-16">
        <div class="mx-auto grid w-full max-w-3xl gap-8 px-4 sm:max-w-155 sm:px-6 md:max-w-170 md:px-6 lg:max-w-7xl lg:grid-cols-[1.1fr_0.9fr] lg:items-start lg:gap-12 lg:px-10">
          <div class="max-w-xl text-(--text-hero) sm:max-w-155 md:max-w-170 lg:pt-18">
            <p class="text-sm font-semibold uppercase tracking-[0.24em] text-(--text-accent-soft)">
              Начнем
            </p>
            <h1 class="mt-4 text-4xl font-black uppercase leading-[0.95] tracking-[-0.04em] sm:text-6xl">
              {{ isLogin ? 'Вход в личный кабинет' : 'Создание аккаунта' }}
            </h1>
            <p class="mt-5 text-base leading-7 text-(--text-accent-soft) sm:text-lg">
              {{ isLogin
                ? 'Войдите, чтобы получить персональные рекомендации по вакансиям.'
                : 'Зарегистрируйтесь, чтобы пройти тест и сохранить результаты в личном кабинете.' }}
            </p>
          </div>

          <div class="rounded-4xl bg-(--surface) px-5 py-6 shadow-(--shadow-card) transition-colors duration-300 sm:mx-auto sm:w-full sm:max-w-155 sm:px-8 sm:py-9 md:max-w-170 lg:max-w-none">
            <div class="mb-8 flex gap-6 border-b border-(--border-soft) pb-4 text-lg font-bold uppercase">
              <button
                type="button"
                class="relative pb-1 transition"
                :class="isLogin ? 'text-(--text-main)' : 'text-(--text-muted)'"
                @click="mode = 'login'"
              >
                Вход
                <span
                  v-if="isLogin"
                  class="absolute inset-x-0 -bottom-4.25 h-1 rounded-full bg-(--button-secondary)"
                />
              </button>
              <button
                type="button"
                class="relative pb-1 transition"
                :class="!isLogin ? 'text-(--text-main)' : 'text-(--text-muted)'"
                @click="mode = 'register'"
              >
                Регистрация
                <span
                  v-if="!isLogin"
                  class="absolute inset-x-0 -bottom-4.25 h-1 rounded-full bg-(--button-secondary)"
                />
              </button>
            </div>

            <form class="space-y-4" @submit.prevent>
                <label class="block">
                  <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Логин</span>
                  <input
                    type="text"
                    placeholder="Логин"
                    class="h-12 w-full rounded-xl border border-transparent bg-(--surface-soft) px-4 text-sm text-(--text-main) outline-none transition placeholder:text-(--text-muted) focus:border-(--button-secondary)"
                  />
                </label>

              <label class="block">
                <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Пароль</span>
                <input
                  type="password"
                  placeholder="Введите пароль"
                  class="h-12 w-full rounded-xl border border-transparent bg-(--surface-soft) px-4 text-sm text-(--text-main) outline-none transition placeholder:text-(--text-muted) focus:border-(--button-secondary)"
                />
              </label>

              <label v-if="!isLogin" class="block">
                <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Повторите пароль</span>
                <input
                  type="password"
                  placeholder="Повторите пароль"
                  class="h-12 w-full rounded-xl border border-transparent bg-(--surface-soft) px-4 text-sm text-(--text-main) outline-none transition placeholder:text-(--text-muted) focus:border-(--button-secondary)"
                />
              </label>

              <button
                type="submit"
                class="mt-2 flex h-12 w-full items-center justify-center rounded-xl bg-(--button-secondary) text-sm font-bold uppercase tracking-[0.08em] text-(--button-text) shadow-[0_12px_26px_rgba(90,102,255,0.28)] transition hover:bg-(--button-secondary-hover)"
              >
                {{ isLogin ? 'Войти' : 'Зарегистрироваться' }}
              </button>
            </form>

            <p class="mt-4 text-center text-sm text-(--text-accent-soft)">
              {{ isLogin ? 'Нет аккаунта?' : 'Уже есть аккаунт?' }}
              <button
                type="button"
                class="font-semibold text-(--button-secondary) transition hover:text-(--button-secondary-hover)"
                @click="toggleMode"
              >
                {{ isLogin ? 'Регистрация' : 'Вход' }}
              </button>
            </p>
          </div>
        </div>
      </section>
    </main>

    <SiteFooter />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

import SiteFooter from '@/components/SiteFooter.vue'
import SiteHeader from '@/components/ThemedSiteHeader.vue'

const mode = ref('register')

const isLogin = computed(() => mode.value === 'login')

function toggleMode() {
  mode.value = isLogin.value ? 'register' : 'login'
}
</script>

