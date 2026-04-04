<template>
  <div
    class="flex flex-col bg-(--page-bg) transition-colors duration-300"
    :class="isAuthenticated ? 'min-h-screen' : 'h-screen overflow-hidden'"
  >
    <SiteHeader />

    <main class="flex min-h-0 flex-1">
      <section
        ref="heroSectionRef"
        class="homepage-hero relative box-border min-h-0 flex-1 px-0 sm:px-10 lg:px-32"
        :class="isAuthenticated ? 'overflow-x-hidden py-16 sm:py-20 lg:py-24' : 'flex items-center overflow-hidden py-10 sm:py-14 lg:py-16'"
        @pointermove="handlePointerMove"
        @pointerleave="resetPointerOffset"
      >
        <div
          class="homepage-hero__background"
          :class="{ 'homepage-hero__background--dark': isDark }"
          :style="backgroundStyle"
          aria-hidden="true"
        />

        <div class="relative z-10 mx-auto w-full max-w-7xl px-4 sm:px-6 md:px-10 lg:px-10">
          <template v-if="isAuthenticated">
            <div class="mt-4">
              <h1 class="text-4xl font-black uppercase leading-[1.02] tracking-[-0.03em] text-(--text-hero) sm:text-6xl lg:text-7xl">
                Ваши данные
              </h1>
              <p class="mt-5 text-base leading-7 text-(--text-main)/80 sm:max-w-4xl sm:text-lg sm:leading-8">
                {{ headerSummary }}
              </p>
              <p class="mt-5 text-base uppercase leading-snug tracking-[0.03em] text-(--text-body) sm:text-2xl">
                Самая подходящая специальность - {{ bestSpecialty }}
              </p>
            </div>

            <div
              v-if="isResultsLoading"
              class="mt-12 flex min-h-90 items-center justify-center rounded-4xl bg-(--surface) p-8 text-center shadow-(--shadow-card)"
            >
              <div>
                <div class="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-(--button-secondary)/20 border-t-(--button-secondary)" />
                <p class="mt-5 text-xs font-semibold uppercase tracking-[0.24em] text-(--text-accent-soft)">
                  Формируем персональный результат
                </p>
                <p class="mt-3 text-sm text-(--text-main)/70">
                  {{ loadingMessage }}
                </p>
              </div>
            </div>

            <div
              v-else-if="jobError"
              class="mt-12 rounded-4xl border border-rose-400/35 bg-rose-500/8 p-6 text-rose-700 shadow-(--shadow-card) dark:text-rose-200"
            >
              {{ jobError }}
            </div>

            <template v-else>
              <div class="mt-12 grid items-start gap-5 lg:grid-cols-[0.72fr_1.8fr] lg:gap-8">
                <article class="self-start rounded-4xl bg-(--surface) p-6 shadow-(--shadow-card) sm:p-8">
                  <h2 class="text-lg font-black uppercase tracking-[0.28em] text-(--text-hero) sm:text-2xl">
                    О вас
                  </h2>
                  <ul class="mt-6 space-y-3 text-sm leading-6 text-(--text-main)/72 sm:text-lg sm:leading-8">
                    <li>Возраст: {{ aboutUser.age }}</li>
                    <li>Опыт: {{ aboutUser.experience }}</li>
                    <li>Образование: {{ aboutUser.education }}</li>
                  </ul>

                  <div class="mt-6">
                    <p class="text-sm font-semibold uppercase tracking-[0.18em] text-(--text-accent-soft)">
                      Сильные стороны
                    </p>
                    <div class="mt-3 flex flex-wrap gap-2">
                      <span
                        v-for="strength in aboutUser.strengths"
                        :key="strength"
                        class="rounded-full bg-(--surface-soft) px-3 py-2 text-xs font-semibold text-(--text-main) sm:text-sm"
                      >
                        {{ strength }}
                      </span>
                    </div>
                  </div>
                </article>

                <article class="rounded-4xl bg-(--surface) p-6 shadow-(--shadow-card) sm:p-8">
                  <h2 class="max-w-5xl text-lg font-black uppercase leading-[1.05] tracking-[0.28em] text-(--text-hero) sm:text-2xl">
                    Проф. склонности, подходящие направления в работе
                  </h2>
                  <div class="mt-6 max-w-5xl space-y-6 text-sm leading-6 text-(--text-main)/75 sm:text-base sm:leading-7">
                    <p>{{ careerFit.summary }}</p>

                    <div>
                      <p class="font-semibold text-(--text-hero)">Ваши шкалы</p>
                      <div class="mt-4 space-y-4">
                        <div
                          v-for="score in displayScores"
                          :key="score.key"
                          class="rounded-3xl border p-4 transition"
                          :class="dominantCategorySet.has(score.key) ? 'border-(--button-secondary)/45 bg-(--button-secondary)/7' : 'border-(--border-soft) bg-(--surface-soft-2)'"
                        >
                          <div class="flex items-center justify-between gap-4">
                            <div class="min-w-0">
                              <p class="font-semibold text-(--text-hero)">{{ score.title }}</p>
                              <p class="mt-1 text-sm leading-6 text-(--text-main)/72">{{ score.label }}</p>
                            </div>
                            <div class="shrink-0 text-sm font-bold text-(--text-hero)">
                              {{ score.score }}/12
                            </div>
                          </div>
                          <div class="mt-3 h-2.5 rounded-full bg-(--surface-soft)">
                            <div
                              class="h-full rounded-full transition-[width]"
                              :class="dominantCategorySet.has(score.key) ? 'bg-(--button-secondary)' : 'bg-(--text-muted)/45'"
                              :style="{ width: `${(score.score / 12) * 100}%` }"
                            />
                          </div>
                        </div>
                      </div>
                    </div>

                    <div>
                      <p class="font-semibold text-(--text-hero)">Профессии подходящие для вас:</p>
                      <div class="mt-3 flex flex-wrap gap-2">
                        <span
                          v-for="profession in careerFit.professions"
                          :key="profession"
                          class="rounded-full bg-(--surface-soft) px-3 py-2 text-sm font-medium text-(--text-main)"
                        >
                          {{ profession }}
                        </span>
                      </div>
                    </div>
                  </div>
                </article>
              </div>

              <article class="mt-8 rounded-4xl bg-(--surface) p-6 shadow-(--shadow-card) sm:p-8">
                <h2 class="max-w-5xl text-lg font-black uppercase leading-[1.05] tracking-[0.28em] text-(--text-hero) sm:text-2xl">
                  Рекомендации как улучшить навыки, повысить квалификацию
                </h2>
                <div class="mt-6 max-w-5xl space-y-5 text-sm leading-6 text-(--text-main)/75 sm:text-base sm:leading-7">
                  <div>
                    <p class="mt-2">{{ developmentRecommendations.summary }}</p>
                  </div>
                  <div>
                    <p class="font-semibold text-(--text-hero)">Как можно повысить квалификацию?</p>
                    <ol class="mt-3 space-y-2">
                      <li v-for="(step, index) in developmentRecommendations.steps" :key="step">
                        {{ index + 1 }}. {{ step }}
                      </li>
                    </ol>
                  </div>
                </div>
              </article>

              <div class="mt-10 rounded-4xl px-6 py-8 text-center sm:px-10 sm:py-10">
                <p class="text-lg uppercase leading-snug tracking-[0.03em] text-(--text-hero) sm:text-3xl">
                  Хотите посмотреть
                  <RouterLink
                    to="/vacancies"
                    class="underline decoration-current decoration-2 underline-offset-4 transition hover:opacity-75"
                    style="text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 4px;"
                  >
                    вакансии
                  </RouterLink>,
                  которые подойдут вам прямо сейчас?
                </p>
              </div>
            </template>
          </template>

          <template v-else>
            <h1
              class="mt-8 text-4xl font-black uppercase leading-[1.06] tracking-[0.02em] text-(--text-hero) sm:mt-12 sm:text-7xl lg:text-7xl"
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
          </template>
        </div>
      </section>
    </main>

    <SiteFooter />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import backgroundObjectDark from '@/assets/background-object-dark.png'
import backgroundObjectLight from '@/assets/background-object-light.png'
import SiteFooter from '@/components/SiteFooter.vue'
import SiteHeader from '@/components/ThemedSiteHeader.vue'
import { useTheme } from '@/composables/useTheme'
import { readAiJobResult, readAiJobStatus, readLatestTestResult } from '@/lib/api'
import {
  STORAGE_KEYS,
  readStorageJson,
  readStorageValue,
  writeStorageJson,
  writeStorageValue,
} from '@/lib/storage'

const { isDark } = useTheme()

const heroSectionRef = ref(null)
const isInteractive = ref(false)
const isAuthenticated = ref(false)
const isResultsLoading = ref(false)
const pointerOffset = ref({ x: 0, y: 0 })
const previewResult = ref(readStorageJson(STORAGE_KEYS.testPreview))
const fullResult = ref(readStorageJson(STORAGE_KEYS.testResult))
const profileDraft = ref(readStorageJson(STORAGE_KEYS.profileDraft, {}))
const authUser = ref(readStorageJson(STORAGE_KEYS.authUser))
const authJob = ref(readStorageJson(STORAGE_KEYS.authJob))
const jobError = ref('')

let animationFrameId = 0
let mediaQueryList = null
let pollingTimeoutId = 0
let currentOffsetX = 0
let currentOffsetY = 0
let targetOffsetX = 0
let targetOffsetY = 0

const backgroundStyle = computed(() => ({
  '--homepage-bg-image': `url(${isDark.value ? backgroundObjectDark : backgroundObjectLight})`,
  '--homepage-bg-offset-x': `${pointerOffset.value.x}px`,
  '--homepage-bg-offset-y': `${pointerOffset.value.y}px`,
}))

const headerSummary = computed(
  () =>
    fullResult.value?.preview_summary ??
    previewResult.value?.preview_summary ??
    'После прохождения теста здесь появится краткий итог по вашему профилю.',
)

const bestSpecialty = computed(
  () =>
    fullResult.value?.best_specialty ??
    previewResult.value?.dominant_categories?.[0] ??
    'результат теста',
)

const aboutUser = computed(() => ({
  age: fullResult.value?.about_user?.age ?? (profileDraft.value?.age ? `${profileDraft.value.age} лет` : 'не указано'),
  experience:
    fullResult.value?.about_user?.experience ??
    formatWorkExperience(profileDraft.value?.workExperienceMonths ?? authUser.value?.work_experience),
  education:
    fullResult.value?.about_user?.education ??
    formatEducationLevel(profileDraft.value?.educationLevel ?? authUser.value?.education_level),
  strengths:
    fullResult.value?.about_user?.strengths ??
    (profileDraft.value?.hobbiesText ? profileDraft.value.hobbiesText.split(',').map((item) => item.trim()).filter(Boolean) : ['Результат ещё формируется']),
}))

const displayScores = computed(() => fullResult.value?.scores ?? previewResult.value?.scores ?? [])
const dominantCategorySet = computed(
  () => new Set(fullResult.value?.dominant_categories ?? previewResult.value?.dominant_categories ?? []),
)

const careerFit = computed(() => ({
  title: fullResult.value?.career_fit?.title ?? 'Проф. склонности, подходящие направления в работе,',
  summary:
    fullResult.value?.career_fit?.summary ??
    'После полной обработки результата здесь появится развёрнутое описание ваших склонностей.',
  professions: fullResult.value?.career_fit?.professions ?? [],
}))

const developmentRecommendations = computed(() => ({
  title: fullResult.value?.development_recommendations?.title ?? 'Рекомендации как улучшить навыки, повысить квалификацию',
  summary:
    fullResult.value?.development_recommendations?.summary ??
    'После обработки результата мы подготовим персональные рекомендации по развитию.',
  steps:
    fullResult.value?.development_recommendations?.steps ?? [
      'Дождитесь завершения формирования персонального результата.',
      'После этого здесь появятся три конкретных шага развития.',
      'Также мы добавим подборку подходящих вакансий.',
    ],
}))

const vacancies = computed(() => fullResult.value?.vacancies ?? [])
const loadingMessage = computed(() => {
  const status = authJob.value?.jobStatus

  if (status === 'processing') {
    return 'Нейросеть сейчас подготавливает персональные рекомендации.'
  }

  return 'Собираем итог по результатам теста и данным профиля.'
})

function animateBackground() {
  currentOffsetX += (targetOffsetX - currentOffsetX) * 0.08
  currentOffsetY += (targetOffsetY - currentOffsetY) * 0.08

  pointerOffset.value = {
    x: Number(currentOffsetX.toFixed(2)),
    y: Number(currentOffsetY.toFixed(2)),
  }

  animationFrameId = window.requestAnimationFrame(animateBackground)
}

function updateInteractivity() {
  if (!mediaQueryList) {
    return
  }

  isInteractive.value = mediaQueryList.matches

  if (!isInteractive.value) {
    targetOffsetX = 0
    targetOffsetY = 0
    currentOffsetX = 0
    currentOffsetY = 0
    pointerOffset.value = { x: 0, y: 0 }
  }
}

function handlePointerMove(event) {
  if (!isInteractive.value || !heroSectionRef.value) {
    return
  }

  const bounds = heroSectionRef.value.getBoundingClientRect()
  const relativeX = (event.clientX - bounds.left) / bounds.width - 0.5
  const relativeY = (event.clientY - bounds.top) / bounds.height - 0.5

  targetOffsetX = -relativeX * 48
  targetOffsetY = -relativeY * 40
}

function resetPointerOffset() {
  targetOffsetX = 0
  targetOffsetY = 0
}

function syncAuthState() {
  isAuthenticated.value = readStorageValue(STORAGE_KEYS.authFlag) === 'true'
  isResultsLoading.value = readStorageValue(STORAGE_KEYS.authLoading) === 'true'
  previewResult.value = readStorageJson(STORAGE_KEYS.testPreview)
  fullResult.value = readStorageJson(STORAGE_KEYS.testResult)
  profileDraft.value = readStorageJson(STORAGE_KEYS.profileDraft, {})
  authUser.value = readStorageJson(STORAGE_KEYS.authUser)
  authJob.value = readStorageJson(STORAGE_KEYS.authJob)
}

function persistFullResult(result) {
  fullResult.value = result
  writeStorageJson(STORAGE_KEYS.testResult, result)
}

function finishLoading() {
  isResultsLoading.value = false
  writeStorageValue(STORAGE_KEYS.authLoading, 'false')
}

function scheduleNextPoll(jobId) {
  pollingTimeoutId = window.setTimeout(() => {
    pollJob(jobId)
  }, 2500)
}

async function pollJob(jobId) {
  try {
    const status = await readAiJobStatus(jobId)
    authJob.value = {
      jobId,
      jobStatus: status.status,
    }
    writeStorageJson(STORAGE_KEYS.authJob, authJob.value)

    if (status.status === 'pending' || status.status === 'processing') {
      scheduleNextPoll(jobId)
      return
    }

    if (status.status === 'failed') {
      jobError.value = status.error_message ?? 'Не удалось сформировать полный результат.'
      finishLoading()
      return
    }

    if (status.status === 'ready') {
      const result = await readAiJobResult(jobId)
      persistFullResult(result)
      finishLoading()
    }
  } catch (error) {
    jobError.value = error?.message ?? 'Не удалось получить статус формирования результата.'
    finishLoading()
  }
}

async function loadLatestResult() {
  const token = readStorageValue(STORAGE_KEYS.accessToken)

  if (!token) {
    return
  }

  try {
    const result = await readLatestTestResult(token)
    persistFullResult(result)
  } catch {
    if (!fullResult.value) {
      jobError.value = 'Не удалось загрузить сохранённый результат.'
    }
  }
}

function startAuthFlow() {
  if (!isAuthenticated.value) {
    return
  }

  if (pollingTimeoutId) {
    window.clearTimeout(pollingTimeoutId)
    pollingTimeoutId = 0
  }

  if (isResultsLoading.value && authJob.value?.jobId) {
    jobError.value = ''
    pollJob(authJob.value.jobId)
    return
  }

  if (isResultsLoading.value && !authJob.value?.jobId) {
    loadLatestResult().finally(() => {
      finishLoading()
    })
    return
  }

  if (!isResultsLoading.value && !fullResult.value) {
    loadLatestResult()
  }
}

function handleStorageChange() {
  syncAuthState()
  startAuthFlow()
}

function formatEducationLevel(value) {
  const map = {
    school: 'школа',
    college: 'колледж',
    bachelor: 'бакалавриат',
    master: 'магистратура',
    specialist: 'специалитет',
  }

  return value ? map[value] ?? value : 'не указано'
}

function formatWorkExperience(monthsValue) {
  const months = Number(monthsValue)

  if (!Number.isFinite(months) || months <= 0) {
    return 'без опыта'
  }

  const years = Math.floor(months / 12)
  const restMonths = months % 12

  if (years && restMonths) {
    return `${years} г. ${restMonths} мес.`
  }

  if (years) {
    return `${years} г.`
  }

  return `${restMonths} мес.`
}

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

onMounted(() => {
  mediaQueryList = window.matchMedia('(min-width: 768px) and (pointer: fine)')
  handleStorageChange()
  updateInteractivity()
  mediaQueryList.addEventListener('change', updateInteractivity)
  window.addEventListener('storage', handleStorageChange)
  animationFrameId = window.requestAnimationFrame(animateBackground)
})

onBeforeUnmount(() => {
  if (animationFrameId) {
    window.cancelAnimationFrame(animationFrameId)
  }

  if (pollingTimeoutId) {
    window.clearTimeout(pollingTimeoutId)
  }

  mediaQueryList?.removeEventListener('change', updateInteractivity)
  window.removeEventListener('storage', handleStorageChange)
})
</script>

<style scoped>
.homepage-hero {
  isolation: isolate;
}

.homepage-hero__background {
  position: absolute;
  inset: 44% auto auto 50%;
  width: min(88vw, 1120px);
  aspect-ratio: 1 / 1;
  background-image: var(--homepage-bg-image);
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  opacity: 0.92;
  pointer-events: none;
  transform: translate3d(
    calc(-50% + var(--homepage-bg-offset-x, 0px)),
    calc(-50% + var(--homepage-bg-offset-y, 0px)),
    0
  );
  transition: opacity 0.3s ease;
  z-index: 0;
}

.homepage-hero__background--dark {
  opacity: 0.88;
}

@media (max-width: 767px), (pointer: coarse) {
  .homepage-hero__background {
    width: min(135vw, 820px);
    opacity: 0.82;
    transform: translate3d(-50%, -44%, 0);
  }
}
</style>
