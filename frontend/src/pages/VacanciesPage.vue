<template>
  <div class="vacancies-page flex min-h-screen flex-col">
    <SiteHeader />

    <main class="flex flex-1">
      <section class="flex flex-1 px-0 py-10 sm:px-10 sm:py-14 lg:px-32 lg:py-16">
        <div class="mx-auto w-full max-w-7xl px-4 sm:px-6 md:px-10 lg:px-10">
          <h1 class="vacancies-page__title mt-10 text-4xl font-black uppercase leading-[1.02] tracking-[-0.03em] sm:mt-20 sm:text-6xl">
            Подобрали самые удачные вакансии для вас!
          </h1>

          <div
            v-if="!vacancies.length"
            class="vacancies-empty mt-12 rounded-[2rem] px-6 py-6 sm:px-8 sm:py-8"
          >
            Список вакансий пока пуст. Завершите формирование полного результата, и здесь появятся подходящие предложения.
          </div>

          <div v-else class="mt-10 space-y-8">
            <article
              v-for="vacancy in vacancies"
              :key="vacancy.hh_vacancy_id"
              class="vacancy-card"
            >
              <div class="vacancy-card__content">
                <div class="vacancy-card__main">
                  <h2 class="vacancy-card__title">
                    {{ vacancy.title }}
                  </h2>

                  <p class="vacancy-card__meta">
                    {{ vacancy.employer_name || 'Компания не указана' }}
                  </p>
                  <p class="vacancy-card__meta">
                    {{ vacancy.area_name || 'Город, район не указан' }}
                  </p>

                  <p
                    v-if="vacancy.snippet?.requirement"
                    class="vacancy-card__snippet"
                  >
                    {{ vacancy.snippet.requirement }}
                  </p>
                  <p
                    v-if="vacancy.snippet?.responsibility"
                    class="vacancy-card__snippet"
                  >
                    {{ vacancy.snippet.responsibility }}
                  </p>
                </div>

                <a
                  :href="vacancy.alternate_url"
                  target="_blank"
                  rel="noreferrer"
                  class="vacancy-card__action"
                >
                  Откликнуться
                </a>
              </div>
            </article>
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
</script>

<style scoped>
.vacancies-page {
  background: linear-gradient(135deg, #161455 0%, #21176e 34%, #4a1d67 62%, #241782 100%);
  color: #fff;
}

.vacancies-page__title {
  max-width: 52rem;
  color: #fff3fa;
}

.vacancies-empty,
.vacancy-card {
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: linear-gradient(180deg, rgba(237, 183, 255, 0.18), rgba(237, 183, 255, 0.1));
  box-shadow: 0 24px 64px rgba(9, 5, 40, 0.22);
  backdrop-filter: blur(18px);
}

.vacancy-card {
  border-radius: 2rem;
  padding: 1.8rem 1.9rem;
}

.vacancy-card__content {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem;
}

.vacancy-card__main {
  min-width: 0;
}

.vacancy-card__title {
  margin: 0;
  color: #fff;
  font-size: clamp(1.8rem, 2.6vw, 2.2rem);
  font-weight: 800;
  line-height: 1.08;
}

.vacancy-card__meta {
  margin: 0.55rem 0 0;
  color: rgba(255, 255, 255, 0.86);
  font-size: 1rem;
  line-height: 1.35;
}

.vacancy-card__snippet {
  margin: 1rem 0 0;
  max-width: 42rem;
  color: rgba(255, 255, 255, 0.82);
  font-size: 0.96rem;
  line-height: 1.45;
}

.vacancy-card__action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 12.5rem;
  min-height: 3.15rem;
  border-radius: 9999px;
  background: linear-gradient(180deg, #587bff 0%, #5065ff 100%);
  padding: 0 1.6rem;
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.vacancy-card__action:hover {
  transform: translateY(-1px);
}

@media (max-width: 767px) {
  .vacancies-page__title {
    max-width: 20rem;
  }

  .vacancy-card {
    border-radius: 1.6rem;
    padding: 1.25rem 1rem;
  }

  .vacancy-card__content {
    flex-direction: column;
    align-items: stretch;
    gap: 1.2rem;
  }

  .vacancy-card__title {
    font-size: 1.5rem;
  }

  .vacancy-card__meta {
    font-size: 0.96rem;
  }

  .vacancy-card__action {
    width: 100%;
    min-width: 0;
  }
}
</style>
