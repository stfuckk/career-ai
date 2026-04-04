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
          <div class="absolute top-0 right-4 z-20 sm:right-6 md:right-10 lg:right-10">
            <div class="rounded-full bg-(--surface) px-4 py-2 shadow-(--shadow-card) transition-colors duration-300">
              <div class="flex items-center gap-3">
                <span class="text-xs font-semibold uppercase tracking-[0.16em] text-(--text-accent-soft)">
                  Тестовый вход
                </span>
                <button
                  type="button"
                  class="relative h-8 w-15 rounded-full transition-colors duration-300"
                  :class="isAuthenticated ? 'bg-(--button-secondary)' : 'bg-(--surface-soft)'"
                  :aria-pressed="isAuthenticated"
                  @click="toggleAuthState"
                >
                  <span
                    class="absolute top-1 left-1 h-6 w-6 rounded-full bg-white shadow-md transition-transform duration-300"
                    :class="isAuthenticated ? 'translate-x-7' : 'translate-x-0'"
                  />
                </button>
              </div>
            </div>
          </div>

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

            <div class="mt-12 grid gap-5 lg:grid-cols-[0.7fr_1.8fr] lg:gap-8">
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

            <article class="mt-8 rounded-4xl bg-(--surface) p-6 shadow-(--shadow-card) sm:p-8">
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

const { isDark } = useTheme()
const AUTH_STORAGE_KEY = 'career-ai-demo-auth'

const primaryRecommendation = 'разработчик на питоне'
const profileSummary = [
  'Возраст: 22 года',
  'Опыт: 1,5 года в IT-секторе',
  'Сильные стороны: системное мышление, интерес к автоматизации, базовое владение синтаксисом.',
  'Образование: бакалавриат',
]
const profileDescription =
  'Ваши проф. склонности: высокий уровень логического анализа, склонность к работе с алгоритмами и структурированными данными. Способность к быстрому освоению новых библиотек.'
const recommendedRoles = [
  'Python Backend Developer',
  'Data Engineer',
  'Automation QA (Python)',
  'DevOps Engineer',
  'Data Analyst',
]
const recommendationIntro =
  'Ваш текущий фундамент позволяет совершить быстрый переход в разработку. Мы рекомендуем сфокусироваться на backend-направлении и постепенно усиливать знания по работе с API и базами данных.'
const improvementSteps = [
  'Реализуйте проект с сервисом доставки и использованием асинхронности.',
  'Изучите Docker для контейнеризации своих приложений.',
  'Пройдите курс по архитектуре распределенных систем.',
]

const heroSectionRef = ref(null)
const isInteractive = ref(false)
const isAuthenticated = ref(false)
const pointerOffset = ref({ x: 0, y: 0 })

let animationFrameId = 0
let mediaQueryList = null
let currentOffsetX = 0
let currentOffsetY = 0
let targetOffsetX = 0
let targetOffsetY = 0

const backgroundStyle = computed(() => ({
  '--homepage-bg-image': `url(${isDark.value ? backgroundObjectDark : backgroundObjectLight})`,
  '--homepage-bg-offset-x': `${pointerOffset.value.x}px`,
  '--homepage-bg-offset-y': `${pointerOffset.value.y}px`,
}))

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
  if (typeof window === 'undefined') {
    return
  }

  isAuthenticated.value = window.localStorage.getItem(AUTH_STORAGE_KEY) === 'true'
}

function toggleAuthState() {
  if (typeof window === 'undefined') {
    return
  }

  const nextValue = !isAuthenticated.value
  window.localStorage.setItem(AUTH_STORAGE_KEY, String(nextValue))
  isAuthenticated.value = nextValue
}

onMounted(() => {
  mediaQueryList = window.matchMedia('(min-width: 768px) and (pointer: fine)')
  syncAuthState()
  updateInteractivity()
  mediaQueryList.addEventListener('change', updateInteractivity)
  animationFrameId = window.requestAnimationFrame(animateBackground)
})

onBeforeUnmount(() => {
  if (animationFrameId) {
    window.cancelAnimationFrame(animationFrameId)
  }

  mediaQueryList?.removeEventListener('change', updateInteractivity)
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
