<template>
  <div class="flex min-h-screen flex-col bg-(--page-bg-alt) transition-colors duration-300">
    <SiteHeader />

    <main class="flex flex-1">
      <section class="flex flex-1 px-0 py-10 sm:px-10 sm:py-14 lg:px-32 lg:py-16">
        <div class="mx-auto w-full max-w-7xl px-4 sm:px-6 md:px-10 lg:px-10">
          <h1 class="text-4xl font-black uppercase leading-[1.02] tracking-[-0.03em] text-(--text-hero) sm:text-6xl lg:text-7xl">
            Вакансии
          </h1>
          <p class="mt-5 max-w-4xl text-base leading-7 text-(--text-main)/80 sm:text-lg sm:leading-8">
            Здесь собраны вакансии, которые подходят вашему текущему профилю и результатам теста.
          </p>

          <div
            v-if="!vacancies.length"
            class="mt-10 rounded-4xl bg-(--surface) p-6 text-(--text-main)/75 shadow-(--shadow-card) sm:p-8"
          >
            Список вакансий пока пуст. Завершите регистрацию и дождитесь формирования полного результата.
          </div>

          <div v-else class="mt-10 grid gap-4 lg:grid-cols-2">
            <a
              v-for="vacancy in vacancies"
              :key="vacancy.hh_vacancy_id"
              :href="vacancy.alternate_url"
              target="_blank"
              rel="noreferrer"
              class="rounded-3xl border border-(--border-soft) bg-(--surface) p-5 shadow-(--shadow-card) transition hover:border-(--button-secondary)/40"
            >
              <p class="text-lg font-semibold text-(--text-hero)">{{ vacancy.title }}</p>
              <p v-if="vacancy.employer_name || vacancy.area_name" class="mt-2 text-sm text-(--text-main)/72">
                {{ [vacancy.employer_name, vacancy.area_name].filter(Boolean).join(' • ') }}
              </p>
              <p v-if="vacancy.salary_from || vacancy.salary_to" class="mt-2 text-sm font-medium text-(--text-hero)">
                {{ formatSalary(vacancy) }}
              </p>
              <p
                v-if="vacancy.snippet?.requirement || vacancy.snippet?.responsibility"
                class="mt-3 text-sm leading-6 text-(--text-main)/72"
              >
                {{ vacancy.snippet?.requirement ?? vacancy.snippet?.responsibility }}
              </p>
            </a>
          </div>
        </div>
      </section>
    </main>

    <SiteFooter />
  </div>
</template>

<script setup>
import { computed } from 'vue'

import SiteFooter from '@/components/SiteFooter.vue'
import SiteHeader from '@/components/ThemedSiteHeader.vue'
import { STORAGE_KEYS, readStorageJson } from '@/lib/storage'

const fullResult = readStorageJson(STORAGE_KEYS.testResult)
const vacancies = computed(() => fullResult?.vacancies ?? [])

function formatSalary(vacancy) {
  const parts = []

  if (vacancy.salary_from) {
    parts.push(`от ${vacancy.salary_from}`)
  }

  if (vacancy.salary_to) {
    parts.push(`до ${vacancy.salary_to}`)
  }

  if (vacancy.currency) {
    parts.push(vacancy.currency)
  }

  return parts.join(' ') || 'Зарплата не указана'
}
</script>
