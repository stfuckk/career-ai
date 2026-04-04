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
            <div class="mt-4 sm:mt-4">
              <h1
                class="text-4xl font-black uppercase leading-[1.02] tracking-[-0.03em] text-(--text-hero) sm:text-6xl lg:text-7xl"
              >
                Ваши данные
              </h1>
              <p
                class="mt-6 text-base uppercase leading-snug tracking-[0.03em] text-(--text-body) sm:text-2xl"
              >
                Самая подходящая специальность - {{ primaryRecommendation }}
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
              </div>
            </div>

            <div v-else class="mt-12 grid gap-5 lg:grid-cols-[0.7fr_1.8fr] lg:gap-8">
              <article class="rounded-4xl bg-(--surface) p-6 shadow-(--shadow-card) sm:p-8">
                <h2
                  class="text-lg font-black uppercase tracking-[0.28em] text-(--text-hero) sm:text-2xl"
                >
                  О вас
                </h2>
                <ul class="mt-6 space-y-3 text-sm leading-6 text-(--text-main)/72 sm:text-lg sm:leading-8">
                  <li v-for="item in profileSummary" :key="item">{{ item }}</li>
                </ul>
              </article>

              <article class="rounded-4xl bg-(--surface) p-6 shadow-(--shadow-card) sm:p-8">
                <h2
                  class="max-w-5xl text-lg font-black uppercase leading-[1.05] tracking-[0.28em] text-(--text-hero) sm:text-2xl"
                >
                  Проф. склонности, подходящие направления в работе,
                </h2>
                <div class="mt-6 max-w-4xl space-y-5 text-sm leading-6 text-(--text-main)/72 sm:text-lg sm:leading-8">
                  <p>{{ profileDescription }}</p>
                  <div>
                    <p class="font-semibold text-(--text-hero)">Профессии подходящие для вас:</p>
                    <ol class="mt-2 space-y-1">
                      <li v-for="(item, index) in recommendedRoles" :key="item">
                        {{ index + 1 }}. {{ item }}
                      </li>
                    </ol>
                  </div>
                </div>
              </article>
            </div>

            <article
              v-if="!isResultsLoading"
              class="mt-8 rounded-4xl bg-(--surface) p-6 shadow-(--shadow-card) sm:p-8"
            >
              <h2
                class="max-w-5xl text-lg font-black uppercase leading-[1.05] tracking-[0.28em] text-(--text-hero) sm:text-2xl"
              >
                Рекомендации как улучшить навыки, повысить квалификацию
              </h2>
              <div class="mt-6 max-w-5xl space-y-5 text-sm leading-6 text-(--text-main)/72 sm:text-lg sm:leading-8">
                <div>
                  <p class="font-semibold text-(--text-hero)">
                    Рекомендации специально для вас
                  </p>
                  <p class="mt-2">{{ recommendationIntro }}</p>
                </div>
                <div>
                  <p class="font-semibold text-(--text-hero)">Как можно повысить квалификацию?</p>
                  <ul class="mt-2 space-y-1">
                    <li v-for="item in improvementSteps" :key="item">{{ item }}</li>
                  </ul>
                </div>
              </div>
            </article>
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
import { readLatestTestResult } from '@/lib/api'
import {
  STORAGE_KEYS,
  readStorageJson,
  readStorageValue,
  writeStorageValue,
} from '@/lib/storage'

const { isDark } = useTheme()

const heroSectionRef = ref(null)
const isInteractive = ref(false)
const isAuthenticated = ref(false)
const isResultsLoading = ref(false)
const pointerOffset = ref({ x: 0, y: 0 })
const previewResult = ref(readStorageJson(STORAGE_KEYS.testPreview))
const latestResult = ref(null)
const profileDraft = ref(readStorageJson(STORAGE_KEYS.profileDraft, {}))
const authUser = ref(readStorageJson(STORAGE_KEYS.authUser))

let animationFrameId = 0
let mediaQueryList = null
let authLoadingTimeoutId = 0
let currentOffsetX = 0
let currentOffsetY = 0
let targetOffsetX = 0
let targetOffsetY = 0

const backgroundStyle = computed(() => ({
  '--homepage-bg-image': `url(${isDark.value ? backgroundObjectDark : backgroundObjectLight})`,
  '--homepage-bg-offset-x': `${pointerOffset.value.x}px`,
  '--homepage-bg-offset-y': `${pointerOffset.value.y}px`,
}))

const displayResult = computed(() => latestResult.value ?? previewResult.value)
const profileSummary = computed(() => {
  const items = []

  if (profileDraft.value?.age) {
    items.push(`Возраст: ${profileDraft.value.age} лет`)
  }

  if (profileDraft.value?.sex) {
    items.push(`Пол: ${profileDraft.value.sex === 'male' ? 'мужской' : 'женский'}`)
  }

  if (profileDraft.value?.educationLevel) {
    items.push(`Образование: ${formatEducationLevel(profileDraft.value.educationLevel)}`)
  }

  if (profileDraft.value?.workExperienceMonths || authUser.value?.work_experience) {
    items.push(`Опыт: ${formatWorkExperience(profileDraft.value?.workExperienceMonths ?? authUser.value?.work_experience)}`)
  }

  if (profileDraft.value?.hobbiesText) {
    items.push(`Интересы: ${profileDraft.value.hobbiesText}`)
  }

  if (!items.length) {
    items.push('После регистрации здесь появятся ваши данные из анкеты.')
  }

  return items
})

const primaryRecommendation = computed(() => {
  if (latestResult.value?.professions?.length) {
    return latestResult.value.professions[0].name
  }

  if (displayResult.value?.dominant_categories?.length) {
    return displayResult.value.dominant_categories[0]
  }

  return 'результат теста'
})

const profileDescription = computed(() => {
  if (latestResult.value?.summary) {
    return latestResult.value.summary
  }

  if (previewResult.value?.preview_summary) {
    return previewResult.value.preview_summary
  }

  return 'После прохождения теста и регистрации здесь появится персональная интерпретация результата.'
})

const recommendedRoles = computed(() => {
  if (latestResult.value?.professions?.length) {
    return latestResult.value.professions.map((item) => item.name)
  }

  if (displayResult.value?.scores?.length) {
    return displayResult.value.scores.map((item) => `${item.title}: ${item.score}/12 (${item.label})`)
  }

  return ['После обработки результата здесь появятся подходящие направления.']
})

const recommendationIntro = computed(() => {
  if (displayResult.value?.dominant_categories?.length) {
    return `Сейчас у вас лидируют направления: ${displayResult.value.dominant_categories.join(', ')}. После полной обработки добавим персональные рекомендации по развитию.`
  }

  return 'После обработки результата мы покажем персональные рекомендации именно для вас.'
})

const improvementSteps = computed(() => {
  if (latestResult.value?.professions?.length) {
    return latestResult.value.professions.map((item) => item.rationale)
  }

  return [
    'Сохраните результат теста и следите за обновлением персональных рекомендаций.',
    'После появления полной версии результата мы добавим список навыков для развития.',
    'На следующем этапе здесь появятся подобранные вакансии и учебные маршруты.',
  ]
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
  profileDraft.value = readStorageJson(STORAGE_KEYS.profileDraft, {})
  authUser.value = readStorageJson(STORAGE_KEYS.authUser)
}

function handleStorageChange() {
  syncAuthState()
  loadLatestResult()
  startAuthLoadingIfNeeded()
}

function formatEducationLevel(value) {
  const map = {
    school: 'школа',
    college: 'колледж',
    bachelor: 'бакалавриат',
    master: 'магистратура',
    specialist: 'специалитет',
    other: 'другое',
  }

  return map[value] ?? value
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

async function loadLatestResult() {
  const token = readStorageValue(STORAGE_KEYS.accessToken)

  if (!token) {
    latestResult.value = null
    return
  }

  try {
    latestResult.value = await readLatestTestResult(token)
  } catch {
    latestResult.value = null
  }
}

function startAuthLoadingIfNeeded() {
  if (!isAuthenticated.value || !isResultsLoading.value) {
    return
  }

  if (authLoadingTimeoutId) {
    window.clearTimeout(authLoadingTimeoutId)
  }

  authLoadingTimeoutId = window.setTimeout(() => {
    writeStorageValue(STORAGE_KEYS.authLoading, 'false')
    isResultsLoading.value = false
  }, 1800)
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

  if (authLoadingTimeoutId) {
    window.clearTimeout(authLoadingTimeoutId)
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
