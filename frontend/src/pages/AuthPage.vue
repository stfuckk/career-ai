<template>
  <div class="flex min-h-screen flex-col bg-[#EDEDFF]">
    <SiteHeader />

    <main class="flex-1">
      <section class="px-0 py-10 sm:px-5 sm:py-14 lg:px-32 lg:py-16">
        <div class="mx-auto grid w-full max-w-3xl gap-8 px-4 sm:max-w-[620px] sm:px-6 md:max-w-[680px] md:px-6 lg:max-w-7xl lg:grid-cols-[1.1fr_0.9fr] lg:items-start lg:gap-12 lg:px-10">
          <div class="max-w-xl text-[#1d107e] sm:max-w-[620px] md:max-w-[680px] lg:pt-18">
            <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[#1d107e]/70">
              Начнем
            </p>
            <h1 class="mt-4 text-4xl font-black uppercase leading-[0.95] tracking-[-0.04em] sm:text-6xl">
              {{ isLogin ? 'Вход в личный кабинет' : 'Создание аккаунта' }}
            </h1>
            <p class="mt-5 text-base leading-7 text-[#1d107e]/80 sm:text-lg">
              {{ isLogin
                ? 'Войдите, чтобы получить персональные рекомендации по вакансиям.'
                : 'Зарегистрируйтесь, чтобы пройти тест и сохранить результаты в личном кабинете.' }}
            </p>
          </div>

          <div class="rounded-4xl bg-white px-5 py-6 shadow-[0_20px_40px_rgba(40,32,103,0.18)] sm:mx-auto sm:w-full sm:max-w-[620px] sm:px-8 sm:py-9 md:max-w-[680px] lg:max-w-none">
            <div class="mb-8 flex gap-6 border-b border-[#1d107e]/10 pb-4 text-lg font-bold uppercase">
              <button
                type="button"
                class="relative pb-1 transition"
                :class="isLogin ? 'text-black' : 'text-black/35'"
                @click="mode = 'login'"
              >
                Вход
                <span
                  v-if="isLogin"
                  class="absolute inset-x-0 -bottom-4.25 h-1 rounded-full bg-[#5a66ff]"
                />
              </button>
              <button
                type="button"
                class="relative pb-1 transition"
                :class="!isLogin ? 'text-black' : 'text-black/35'"
                @click="mode = 'register'"
              >
                Регистрация
                <span
                  v-if="!isLogin"
                  class="absolute inset-x-0 -bottom-4.25 h-1 rounded-full bg-[#5a66ff]"
                />
              </button>
            </div>

            <form class="space-y-4" @submit.prevent>
                <label class="block">
                  <span class="mb-2 block text-sm font-medium text-[#1d107e]/70">Логин</span>
                  <input
                    type="text"
                    placeholder="Логин"
                    class="h-12 w-full rounded-xl border border-transparent bg-[#f0f1ff] px-4 text-sm text-[#1b1b1b] outline-none transition placeholder:text-[#8d93b9] focus:border-[#5a66ff]"
                  />
                </label>

              <label class="block">
                <span class="mb-2 block text-sm font-medium text-[#1d107e]/70">Пароль</span>
                <input
                  type="password"
                  placeholder="Введите пароль"
                  class="h-12 w-full rounded-xl border border-transparent bg-[#f0f1ff] px-4 text-sm text-[#1b1b1b] outline-none transition placeholder:text-[#8d93b9] focus:border-[#5a66ff]"
                />
              </label>

              <label v-if="!isLogin" class="block">
                <span class="mb-2 block text-sm font-medium text-[#1d107e]/70">Повторите пароль</span>
                <input
                  type="password"
                  placeholder="Повторите пароль"
                  class="h-12 w-full rounded-xl border border-transparent bg-[#f0f1ff] px-4 text-sm text-[#1b1b1b] outline-none transition placeholder:text-[#8d93b9] focus:border-[#5a66ff]"
                />
              </label>

              <button
                type="submit"
                class="mt-2 flex h-12 w-full items-center justify-center rounded-xl bg-[#5a66ff] text-sm font-bold uppercase tracking-[0.08em] text-white shadow-[0_12px_26px_rgba(90,102,255,0.28)] transition hover:bg-[#4a57f5]"
              >
                {{ isLogin ? 'Войти' : 'Зарегистрироваться' }}
              </button>
            </form>

            <p class="mt-4 text-center text-sm text-[#1d107e]/60">
              {{ isLogin ? 'Нет аккаунта?' : 'Уже есть аккаунт?' }}
              <button
                type="button"
                class="font-semibold text-[#5a66ff] transition hover:text-[#4a57f5]"
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
import SiteHeader from '@/components/SiteHeader.vue'

const mode = ref('login')

const isLogin = computed(() => mode.value === 'login')

function toggleMode() {
  mode.value = isLogin.value ? 'register' : 'login'
}
</script>
