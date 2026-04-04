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

              <article
                v-if="careerPath"
                class="career-path-card mt-8 rounded-[2rem] bg-(--surface) p-6 shadow-(--shadow-card) sm:p-8 lg:p-10"
              >
                <div class="text-center">
                  <p class="text-sm font-black uppercase tracking-[0.42em] text-(--text-hero) sm:text-base">
                    Индивидуальный путь развития
                  </p>
                </div>

                <div class="mt-6 lg:mt-7">
                  <div class="career-path-grid">
                    <div class="career-path-side-note career-path-side-note--current">
                      <span class="career-path-side-note__label">Сейчас вы здесь</span>
                    </div>

                    <div class="career-path-side-note career-path-side-note--future">
                      <span class="career-path-side-note__label">Где можете оказаться</span>
                    </div>

                    <div class="career-path-line" aria-hidden="true" />
                    <svg class="career-path-arrow-overlay career-path-arrow-overlay--current" viewBox="0 0 300 120" aria-hidden="true">
                      <path d="M286 22 C252 54, 214 68, 170 70 C122 72, 80 56, 18 56" />
                      <path d="M30 46 L18 56 L30 66" />
                    </svg>

                    <svg class="career-path-arrow-overlay career-path-arrow-overlay--future" viewBox="0 0 300 120" aria-hidden="true">
                      <path d="M14 98 C48 66, 86 52, 130 50 C178 48, 220 64, 282 64" />
                      <path d="M270 54 L282 64 L270 74" />
                    </svg>

                    <div class="career-path-node career-path-node--current">
                      <div class="career-path-node__marker" aria-hidden="true" />
                      <div class="career-path-node__body">
                        <p class="career-path-node__title">
                          {{ careerPath.currentPosition }}
                        </p>
                      </div>
                    </div>

                    <template v-for="(step, index) in careerPath.steps" :key="`${step.title}-${index}`">
                      <div class="career-path-step">
                        <div class="career-path-step__aside career-path-step__aside--skills">
                          <p class="career-path-step__label">Курсы на повышение навыков</p>
                          <div class="career-path-step__chips">
                            <span
                              v-for="skill in step.skillsToLearn"
                              :key="skill"
                              class="career-path-chip"
                            >
                              {{ skill }}
                            </span>
                          </div>
                        </div>

                        <div class="career-path-node">
                          <div class="career-path-node__marker" aria-hidden="true" />
                          <div class="career-path-node__body">
                            <p class="career-path-node__title">{{ step.title }}</p>
                          </div>
                        </div>

                        <div class="career-path-step__aside career-path-step__aside--vacancies">
                          <p class="career-path-step__label">Вакансии</p>
                          <p class="career-path-step__meta">
                            Опыт: {{ step.experienceRequired }}
                          </p>
                          <p class="career-path-step__query">
                            Запрос: {{ step.hhSearchQuery }}
                          </p>
                        </div>
                      </div>
                    </template>
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

              <div class="mt-4 pb-4 sm:pb-6">
                <button
                  type="button"
                  class="flex min-h-16 w-full items-center justify-center rounded-full bg-(--button-secondary) px-8 text-center text-base font-bold uppercase tracking-[0.08em] text-(--button-text) shadow-[0_16px_32px_rgba(90,102,255,0.28)] transition hover:-translate-y-0.5 hover:bg-(--button-secondary-hover) sm:min-h-20 sm:text-2xl"
                  @click="restartTest"
                >
                  Пройти тест заново
                </button>
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
import { RouterLink, useRouter } from 'vue-router'

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
  removeStorageValue,
  writeStorageJson,
  writeStorageValue,
} from '@/lib/storage'

const { isDark } = useTheme()
const router = useRouter()

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

const careerPath = computed(() => {
  const rawCareerPath = fullResult.value?.career_path

  if (!rawCareerPath?.current_position || !Array.isArray(rawCareerPath?.steps) || !rawCareerPath.steps.length) {
    return null
  }

  return {
    currentPosition: rawCareerPath.current_position,
    steps: rawCareerPath.steps.map((step) => ({
      title: step.title ?? 'Следующая роль',
      skillsToLearn: Array.isArray(step.skills_to_learn) ? step.skills_to_learn.filter(Boolean) : [],
      experienceRequired: step.experience_required ?? 'не указан',
      hhSearchQuery: step.hh_search_query ?? 'не указан',
    })),
  }
})

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

async function restartTest() {
  if (pollingTimeoutId) {
    window.clearTimeout(pollingTimeoutId)
    pollingTimeoutId = 0
  }

  jobError.value = ''
  isResultsLoading.value = false
  previewResult.value = null
  fullResult.value = null
  authJob.value = null

  removeStorageValue(STORAGE_KEYS.testScores)
  removeStorageValue(STORAGE_KEYS.testPreview)
  removeStorageValue(STORAGE_KEYS.testResult)
  removeStorageValue(STORAGE_KEYS.attemptToken)
  removeStorageValue(STORAGE_KEYS.authJob)
  writeStorageValue(STORAGE_KEYS.authLoading, 'false')

  await router.push('/test')
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

.career-path-card {
  position: relative;
  overflow: hidden;
}

.career-path-card::before {
  content: '';
  position: absolute;
  inset: auto auto 12% -4%;
  width: 16rem;
  height: 16rem;
  border-radius: 9999px;
  background: radial-gradient(circle, color-mix(in srgb, var(--button-secondary) 16%, transparent) 0%, transparent 72%);
  pointer-events: none;
  opacity: 0.85;
}

.career-path-card::after {
  content: '';
  position: absolute;
  inset: 6% -2% auto auto;
  width: 14rem;
  height: 14rem;
  border-radius: 9999px;
  background: radial-gradient(circle, color-mix(in srgb, var(--button-primary) 10%, transparent) 0%, transparent 72%);
  pointer-events: none;
  opacity: 0.9;
}

.career-path-grid {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  max-width: 68rem;
  margin: 0 auto;
  padding: 3.6rem 0 5.75rem;
}

.career-path-line {
  position: absolute;
  top: -1.2rem;
  bottom: -1.5rem;
  left: 50%;
  width: 2px;
  transform: translateX(-50%);
  background: linear-gradient(180deg, var(--button-secondary) 0%, color-mix(in srgb, var(--button-secondary) 38%, transparent) 100%);
  opacity: 0.7;
}

.career-path-side-note {
  position: absolute;
  z-index: 2;
  pointer-events: none;
}

.career-path-side-note--current {
  top: 0.15rem;
  right: 1.25rem;
  transform: rotate(-3deg);
}

.career-path-side-note--future {
  bottom: 1.1rem;
  left: 0.5rem;
  transform: rotate(-7deg);
}

.career-path-side-note__label {
  color: #ff6b57;
  font-size: 0.88rem;
  font-weight: 800;
  letter-spacing: 0.38em;
  text-transform: uppercase;
}

.career-path-arrow-overlay {
  position: absolute;
  z-index: 4;
  fill: none;
  stroke: #ff8b6e;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 3;
  opacity: 0.95;
  pointer-events: none;
}

.career-path-arrow-overlay--current {
  top: 0.9rem;
  left: calc(50% - 0.1rem);
  width: 18rem;
  height: 6rem;
}

.career-path-arrow-overlay--future {
  bottom: 0.95rem;
  right: calc(50% - 0.1rem);
  width: 18rem;
  height: 6rem;
}

.career-path-node,
.career-path-step {
  position: relative;
  z-index: 1;
}

.career-path-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.2rem;
  text-align: center;
}

.career-path-node__marker {
  width: 0.9rem;
  height: 0.9rem;
  border-radius: 9999px;
  background: var(--button-secondary);
  box-shadow: 0 0 0 8px color-mix(in srgb, var(--button-secondary) 14%, transparent);
}

.career-path-node--current .career-path-node__marker {
  width: 1.15rem;
  height: 1.15rem;
}

.career-path-node__body {
  max-width: 18rem;
  padding: 0.45rem 1.15rem;
  border-radius: 1.5rem;
  background: color-mix(in srgb, var(--surface) 78%, transparent);
  backdrop-filter: blur(10px);
  box-shadow: 0 0 0 12px color-mix(in srgb, var(--surface) 58%, transparent);
}

.career-path-node__title {
  color: var(--text-hero);
  font-size: clamp(1.25rem, 1.75vw, 1.8rem);
  font-weight: 800;
  line-height: 1.05;
}

.career-path-node__caption {
  margin-top: 0.45rem;
  color: color-mix(in srgb, var(--text-main) 70%, transparent);
  font-size: 0.95rem;
  line-height: 1.4;
}

.career-path-step {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  gap: 1.15rem;
  align-items: center;
  min-height: 8.5rem;
}

.career-path-step__aside {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.career-path-step__aside--skills {
  align-items: flex-end;
  text-align: right;
  padding-right: 1.1rem;
}

.career-path-step__aside--vacancies {
  align-items: flex-start;
  text-align: left;
  padding-left: 1.1rem;
}

.career-path-step__label {
  color: color-mix(in srgb, var(--text-main) 68%, transparent);
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.35;
}

.career-path-step__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  justify-content: flex-end;
}

.career-path-chip {
  border: 1px solid color-mix(in srgb, var(--border-soft) 76%, transparent);
  border-radius: 9999px;
  background: color-mix(in srgb, var(--surface-soft) 88%, transparent);
  padding: 0.38rem 0.72rem;
  color: var(--text-main);
  font-size: 0.8rem;
  line-height: 1.2;
}

.career-path-step__meta,
.career-path-step__query {
  color: color-mix(in srgb, var(--text-main) 68%, transparent);
  font-size: 0.9rem;
  line-height: 1.45;
}

@media (max-width: 1023px) {
  .career-path-grid {
    padding-top: 5rem;
    padding-bottom: 5.5rem;
  }

  .career-path-side-note--current {
    top: 0.4rem;
    right: 50%;
    transform: translateX(45%) rotate(-3deg);
  }

  .career-path-side-note--future {
    bottom: 1rem;
    left: 50%;
    transform: translateX(-62%) rotate(-6deg);
  }

  .career-path-arrow-overlay--current {
    top: 1rem;
    left: calc(50% - 0.15rem);
    transform: none;
  }

  .career-path-arrow-overlay--future {
    right: calc(50% - 0.15rem);
    bottom: 0.6rem;
    transform: none;
  }

  .career-path-step {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    justify-items: center;
  }

  .career-path-step__aside--skills,
  .career-path-step__aside--vacancies {
    align-items: center;
    text-align: center;
    padding-left: 0;
    padding-right: 0;
  }

  .career-path-step__chips {
    justify-content: center;
  }
}

@media (max-width: 767px), (pointer: coarse) {
  .homepage-hero__background {
    width: min(135vw, 820px);
    opacity: 0.82;
    transform: translate3d(-50%, -44%, 0);
  }

  .career-path-card::before,
  .career-path-card::after,
  .career-path-line,
  .career-path-arrow-overlay {
    display: none;
  }

  .career-path-grid {
    gap: 1rem;
    padding: 0.5rem 0 0;
  }

  .career-path-side-note {
    position: static;
    transform: none;
    text-align: center;
  }

  .career-path-side-note--future {
    order: 99;
  }

  .career-path-side-note__label {
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-align: center;
  }

  .career-path-node {
    gap: 0.4rem;
  }

  .career-path-node__body {
    max-width: 100%;
    box-shadow: none;
    padding: 0.2rem 0.65rem;
  }

  .career-path-node__title {
    font-size: 1.15rem;
  }

  .career-path-step {
    gap: 0.65rem;
    padding: 0.8rem 0;
    border-top: 1px solid color-mix(in srgb, var(--border-soft) 62%, transparent);
    min-height: auto;
  }

  .career-path-step__label,
  .career-path-step__meta,
  .career-path-step__query {
    font-size: 0.84rem;
  }

  .career-path-step__chips {
    flex-wrap: nowrap;
    width: 100%;
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 0.25rem;
    scrollbar-width: none;
  }

  .career-path-step__chips::-webkit-scrollbar {
    display: none;
  }
}
</style>
