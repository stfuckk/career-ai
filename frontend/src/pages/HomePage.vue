<template>
  <div class="flex min-h-screen flex-col bg-(--page-bg) transition-colors duration-300">
    <SiteHeader />

    <main class="flex-1">
      <section class="px-0 py-20 sm:px-10 sm:py-30 lg:px-32">
        <div class="mx-auto w-full max-w-7xl px-4 sm:px-6 md:px-10 lg:px-10">
          <h1
            class=" text-4xl font-black uppercase leading-[1.06] tracking-[0.02em] text-(--text-hero) sm:text-7xl lg:text-7xl"
          >
            Тест по определению направления
          </h1>
          <p
            class="mt-6 text-base uppercase leading-snug tracking-[-0.02em] text-(--text-body) sm:mt-8 sm:text-2xl"
          >
            Прохождение этого теста сэкономит вам время и поможет подобрать вакансии специально для
            вас
          </p>

          <div class="mt-12 flex justify-center sm:mt-16">
            <RouterLink
              to="/test"
              class="inline-flex min-h-14 items-center justify-center rounded-full bg-(--button-primary) px-8 text-center text-base uppercase tracking-[0.08em] text-(--button-text) shadow-(--shadow-button) transition hover:-translate-y-0.5 hover:bg-(--button-primary-hover) sm:min-h-16 sm:min-w-100 sm:px-16 sm:text-2xl"
              style="color: var(--button-text)"
            >
              Пройти тест
            </RouterLink>
          </div>
        </div>
      </section>
    </main>

    <SiteFooter />
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

import SiteFooter from '@/components/SiteFooter.vue'
import SiteHeader from '@/components/ThemedSiteHeader.vue'
</script>
