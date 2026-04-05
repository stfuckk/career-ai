<template>
  <div
    class="homepage-page flex flex-col"
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
          v-if="!isAuthenticated"
          class="homepage-hero__background"
          :style="backgroundStyle"
          aria-hidden="true"
        />

        <div class="relative z-10 mx-auto w-full max-w-7xl px-4 sm:px-6 md:px-10 lg:px-10">
          <template v-if="isAuthenticated">
            <div class="mt-4">
              <h1 class="homepage-title text-4xl font-black uppercase leading-[1.02] tracking-[-0.03em] sm:text-6xl lg:text-7xl">
                Ваши данные
              </h1>
              <p class="homepage-subtitle mt-5 text-base font-black uppercase leading-snug tracking-[0.03em] sm:text-2xl">
                Самая подходящая специальность: {{ bestSpecialty }}
              </p>
            </div>

            <div
              v-if="isResultsLoading"
              class="homepage-loading-panel mt-14 flex min-h-64 items-center justify-center p-8 text-center"
            >
              <div>
                <div class="homepage-spinner mx-auto h-12 w-12 animate-spin rounded-full border-4" />
                <p class="homepage-loading-kicker mt-5 text-xs font-semibold uppercase tracking-[0.24em]">
                  Формируем персональный результат
                </p>
                <p class="homepage-loading-text mt-3 text-sm">
                  {{ loadingMessage }}
                </p>
              </div>
            </div>

            <div
              v-else-if="jobError"
              class="homepage-error-panel mt-12 rounded-3xl px-6 py-5"
            >
              {{ jobError }}
            </div>

            <template v-else>
              <section class="mt-14">
                <div class="max-w-3xl">
                  <h2 class="homepage-section-title text-2xl font-black uppercase leading-[1.04] sm:text-3xl">
                    Ваши качества
                  </h2>
                  <p class="homepage-section-text mt-4 max-w-3xl text-sm leading-6 sm:text-lg sm:leading-8">
                    {{ qualitiesText }}
                  </p>
                </div>

                <div class="mx-auto mt-12 max-w-4xl text-center">
                  <h2 class="homepage-section-title text-2xl font-black uppercase leading-[1.04] sm:text-3xl">
                    Профессиональные склонности
                  </h2>
                  <p class="homepage-section-text mt-4 text-sm leading-6 sm:text-lg sm:leading-8">
                    {{ careerFit.summary }}
                  </p>
                </div>

                <div class="mt-14 text-center">
                  <h2 class="homepage-section-title text-2xl font-black uppercase leading-[1.04] sm:text-3xl">
                    Рекомендуемые профессии
                  </h2>
                  <div class="mt-6 flex flex-wrap justify-center gap-4">
                    <span
                      v-for="profession in careerFit.professions"
                      :key="profession"
                      class="homepage-profession-chip rounded-3xl px-6 py-4 text-base font-medium sm:min-w-52 sm:text-2xl"
                    >
                      {{ profession }}
                    </span>
                  </div>
                </div>

                <div class="mt-16 max-w-4xl">
                  <h2 class="homepage-section-title text-2xl font-black uppercase leading-[1.04] sm:text-3xl">
                    Рекомендации как улучшить навыки, повысить квалификацию
                  </h2>
                  <div class="homepage-section-text mt-6 space-y-5 text-sm leading-6 sm:text-lg sm:leading-8">
                    <p>{{ developmentRecommendations.summary }}</p>
                    <p v-for="step in developmentRecommendations.steps" :key="step">
                      {{ step }}
                    </p>
                  </div>
                </div>

                <section
                  v-if="personalPath"
                  class="homepage-path mt-20"
                  aria-labelledby="personal-path-title"
                >
                  <div class="homepage-path__header">
                    <h2
                      id="personal-path-title"
                      class="homepage-section-title homepage-path__title text-3xl font-black uppercase leading-[1.02] sm:text-5xl"
                    >
                      Индивидуальный путь
                    </h2>
                  </div>

                  <div
                    class="homepage-path__canvas"
                    :style="pathLayout ? { minHeight: `${pathLayout.height}px` } : undefined"
                  >
                    <svg
                      v-if="pathLayout"
                      class="homepage-path__diagram"
                      :viewBox="`0 0 1000 ${pathLayout.height}`"
                      aria-hidden="true"
                      preserveAspectRatio="none"
                    >
                      <defs>
                        <marker
                          id="homepage-path-arrowhead"
                          markerWidth="8"
                          markerHeight="8"
                          refX="6"
                          refY="4"
                          orient="auto"
                        >
                          <path
                            d="M0 0L8 4L0 8"
                            fill="none"
                            stroke="#ff2c63"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="1.6"
                          />
                        </marker>
                      </defs>
                      <path
                        v-for="(path, index) in pathLayout.connectorPaths"
                        :key="`connector-${index}`"
                        class="homepage-path__diagram-line"
                        :d="path"
                      />
                      <path
                        v-if="pathLayout.bottomAccentPath"
                        class="homepage-path__diagram-accent"
                        :d="pathLayout.bottomAccentPath"
                      />
                    </svg>

                    <div
                      class="homepage-path__label homepage-path__label--current"
                      :style="pathLayout?.currentLabelStyle"
                    >
                      Сейчас вы можете быть здесь
                    </div>
                    <div
                      class="homepage-path__label homepage-path__label--future"
                      :style="pathLayout?.futureLabelStyle"
                    >
                      Куда можете прийти
                    </div>

                    <article
                      v-for="(step, index) in pathLayout?.nodes ?? []"
                      :key="`${step.title}-${index}`"
                      class="homepage-path__node"
                      :class="[
                        step.side === 'left' ? 'homepage-path__node--left' : 'homepage-path__node--right',
                        step.isCurrent ? 'homepage-path__node--current' : '',
                        step.courses?.length ? 'homepage-path__node--interactive' : '',
                      ]"
                      :style="{ top: `${step.top}px` }"
                      :role="step.courses?.length ? 'button' : undefined"
                      :tabindex="step.courses?.length ? 0 : undefined"
                      @click="openPathCourses(step)"
                      @keydown.enter.prevent="openPathCourses(step)"
                      @keydown.space.prevent="openPathCourses(step)"
                    >
                      <div
                        v-if="step.isCurrent"
                        class="homepage-path__mobile-label homepage-path__mobile-label--current"
                      >
                        Сейчас вы можете быть здесь
                      </div>
                      <div
                        v-else-if="index === (pathLayout?.nodes?.length ?? 0) - 1"
                        class="homepage-path__mobile-label homepage-path__mobile-label--future"
                      >
                        Куда можете прийти
                      </div>
                      <span class="homepage-path__dot" aria-hidden="true" />
                      <h3 class="homepage-path__node-title">
                        {{ step.title }}
                      </h3>
                      <p
                        v-if="step.courses?.length"
                        class="homepage-path__hint"
                      >
                        Нажмите, чтобы посмотреть курсы
                      </p>
                      <div class="homepage-path__chips">
                        <span
                          v-for="badge in step.badges"
                          :key="badge"
                          class="homepage-path__chip"
                        >
                          {{ badge }}
                        </span>
                      </div>
                    </article>
                  </div>
                </section>

                <p class="homepage-vacancies-link mt-18 text-lg sm:text-2xl">
                  Хотите посмотреть список
                  <RouterLink to="/vacancies" class="homepage-vacancies-link__anchor">
                    вакансий
                  </RouterLink>
                  ?
                </p>
              </section>
            </template>
          </template>

          <template v-else>
            <h1
              class="homepage-title mt-8 text-4xl font-black uppercase leading-[1.06] tracking-[0.02em] sm:mt-12 sm:text-7xl lg:text-7xl"
            >
              Тест по определению направления
            </h1>
            <p
              class="homepage-subtitle mt-6 text-base uppercase leading-snug tracking-[-0.02em] sm:mt-8 sm:text-2xl"
            >
              Прохождение этого теста сэкономит вам время и поможет подобрать вакансии специально для
              вас
            </p>

            <div class="mt-12 flex justify-center sm:mt-16">
              <RouterLink
                to="/test"
                class="homepage-cta inline-flex min-h-14 items-center justify-center rounded-full px-8 text-center text-base uppercase tracking-[0.08em] transition hover:-translate-y-0.5 sm:min-h-16 sm:min-w-100 sm:px-16 sm:text-2xl"
              >
                Пройти тест
              </RouterLink>
            </div>
          </template>
        </div>
      </section>
    </main>

    <div
      v-if="selectedPathStep"
      class="homepage-modal"
      @click.self="closePathCourses"
    >
      <div
        class="homepage-modal__panel"
        role="dialog"
        aria-modal="true"
        :aria-label="selectedPathCoursesHeading"
      >
        <button
          type="button"
          class="homepage-modal__close"
          aria-label="Закрыть окно с курсами"
          @click="closePathCourses"
        >
          ×
        </button>

        <div class="homepage-modal__header">
          <p class="homepage-modal__kicker">Курсы для следующего шага</p>
          <h3 class="homepage-modal__title">
            {{ selectedPathCoursesHeading }}
          </h3>
        </div>

        <div
          class="homepage-modal__rail"
          @wheel.stop.prevent="handleCoursesWheel"
        >
          <article
            v-for="course in selectedPathStep.courses"
            :key="course.id"
            class="homepage-course-card"
          >
            <div
              v-if="course.coverUrl"
              class="homepage-course-card__cover"
            >
              <img
                :src="course.coverUrl"
                :alt="course.title"
                class="homepage-course-card__cover-image"
              >
            </div>

            <div class="homepage-course-card__body">
              <div class="homepage-course-card__chips">
                <span
                  v-if="course.skill"
                  class="homepage-course-card__chip"
                >
                  {{ course.skill }}
                </span>
                <span class="homepage-course-card__chip">
                  {{ course.isFree ? 'Бесплатно' : formatCoursePrice(course) }}
                </span>
              </div>

              <component
                :is="course.url ? 'a' : 'h4'"
                :href="course.url || undefined"
                :target="course.url ? '_blank' : undefined"
                :rel="course.url ? 'noreferrer' : undefined"
                class="homepage-course-card__title"
              >
                {{ course.title }}
              </component>

              <p class="homepage-course-card__summary">
                {{ course.summary }}
              </p>

              <div class="homepage-course-card__meta">
                <span v-if="course.learnersCount != null">
                  {{ course.learnersCount }} учеников
                </span>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>

    <SiteFooter />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import backgroundObjectDark from '@/assets/background-object-dark.png'
import SiteFooter from '@/components/SiteFooter.vue'
import SiteHeader from '@/components/ThemedSiteHeader.vue'
import { readAiJobResult, readAiJobStatus, readLatestTestResult } from '@/lib/api'
import {
  STORAGE_KEYS,
  readStorageJson,
  readStorageValue,
  removeStorageValue,
  writeStorageJson,
  writeStorageValue,
} from '@/lib/storage'

const router = useRouter()

const DOMINANT_CATEGORY_LABELS = {
  people: 'Работа с людьми',
  research: 'Исследовательская деятельность',
  practical: 'Практическая деятельность',
  aesthetic: 'Эстетическая деятельность',
  extreme: 'Экстремальная деятельность',
  economic: 'Планово-экономическая деятельность',
}

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
const selectedPathStep = ref(null)

let animationFrameId = 0
let mediaQueryList = null
let pollingTimeoutId = 0
let currentOffsetX = 0
let currentOffsetY = 0
let targetOffsetX = 0
let targetOffsetY = 0

const backgroundStyle = computed(() => ({
  '--homepage-bg-image': `url(${backgroundObjectDark})`,
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
    getDominantCategoryLabel(fullResult.value?.dominant_categories?.[0]) ??
    getDominantCategoryLabel(previewResult.value?.dominant_categories?.[0]) ??
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

const qualitiesText = computed(() => {
  const strengths = Array.isArray(fullResult.value?.about_user?.strengths)
    ? fullResult.value.about_user.strengths.filter(Boolean)
    : []

  if (strengths.length) {
    return strengths.join('. ') + '.'
  }

  return headerSummary.value
})

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
      courses: normalizeCourses(step.courses),
    })),
  }
})

const personalPath = computed(() => {
  if (careerPath.value) {
    return {
      summary: careerFit.value.summary,
      current: {
        title: careerPath.value.currentPosition,
        badges: buildFallbackPathBadges(aboutUser.value.strengths).slice(0, 1),
      },
      future: careerPath.value.steps.slice(0, 3).map((step) => ({
        title: step.title,
        experienceRequired: step.experienceRequired,
        badges: buildPathBadges(step, 2),
        courses: step.courses,
      })),
    }
  }

  const professions = careerFit.value.professions.filter(Boolean)

  if (!professions.length) {
    return null
  }

  return {
    summary: careerFit.value.summary,
    current: {
      title: bestSpecialty.value,
      badges: buildFallbackPathBadges([
        aboutUser.value.experience !== 'не указано' ? `Опыт: ${aboutUser.value.experience}` : null,
      ]),
    },
    future: professions.slice(0, 3).map((profession, index) => ({
      title: profession,
      badges: buildFallbackPathBadges([
        index === 0 ? careerFit.value.title : null,
        index === 1 ? careerFit.value.summary : null,
        index === 2 ? developmentRecommendations.value.steps[0] : null,
      ]),
      courses: [],
    })),
  }
})

const userExperienceMonths = computed(() => {
  const rawMonths = profileDraft.value?.workExperienceMonths ?? authUser.value?.work_experience

  if (rawMonths != null && rawMonths !== '') {
    const numericMonths = Number(rawMonths)

    if (Number.isFinite(numericMonths) && numericMonths >= 0) {
      return numericMonths
    }
  }

  return parseUserExperienceMonths(aboutUser.value.experience)
})

const pathLayout = computed(() => {
  if (!personalPath.value) {
    return null
  }

  const nodes = [
    {
      ...personalPath.value.current,
      isCurrent: true,
    },
    ...personalPath.value.future.map((step) => ({
      ...step,
      isCurrent: false,
    })),
  ]

  const startY = 120
  const verticalGap = 220
  const leftDotX = 300
  const rightDotX = 700

  const layoutNodes = nodes.map((node, index) => {
    const side = index % 2 === 0 ? 'left' : 'right'
    const top = startY + index * verticalGap

    return {
        ...node,
        side,
        top,
        dotX: side === 'left' ? leftDotX : rightDotX,
        dotY: top + 8,
      }
    })

  const currentNodeIndex = findCurrentNodeIndex(layoutNodes, userExperienceMonths.value)
  const currentNode = layoutNodes[currentNodeIndex] ?? layoutNodes[0]

  const connectorPaths = layoutNodes.slice(1).map((node, index) => {
    const prev = layoutNodes[index]
    const horizontalPull = prev.side === 'left' ? 180 : -180

    return [
      `M ${prev.dotX} ${prev.dotY}`,
      `C ${prev.dotX + horizontalPull} ${prev.dotY + 30},`,
      `${node.dotX - horizontalPull} ${node.dotY - 30},`,
      `${node.dotX} ${node.dotY}`,
    ].join(' ')
  })

  const firstFutureNode = layoutNodes[1]
  const lastNode = layoutNodes[layoutNodes.length - 1]
  const futureLabelTop = Math.max(lastNode.top + 92, layoutNodes[0].top + 150)
  const futureLabelStyle = lastNode.side === 'left'
    ? { top: `${futureLabelTop}px`, left: '58%', textAlign: 'left' }
    : { top: `${futureLabelTop}px`, left: '6%', textAlign: 'left' }
  const currentLabelStyle = currentNode.side === 'left'
    ? { top: `${Math.max(currentNode.top - 74, 8)}px`, left: '2.2rem' }
    : { top: `${Math.max(currentNode.top - 74, 8)}px`, right: '2.2rem', left: 'auto', textAlign: 'right' }

  return {
    nodes: layoutNodes,
    connectorPaths,
    height: layoutNodes[layoutNodes.length - 1].top + 220,
    currentLabelStyle,
    futureLabelStyle,
    bottomAccentPath: layoutNodes.length > 2
      ? lastNode.side === 'left'
        ? `M 640 ${futureLabelTop + 92} C 540 ${futureLabelTop + 100}, ${lastNode.dotX + 140} ${lastNode.dotY + 24}, ${lastNode.dotX + 18} ${lastNode.dotY + 2}`
        : `M 180 ${futureLabelTop + 92} C 80 ${futureLabelTop + 100}, ${lastNode.dotX - 140} ${lastNode.dotY + 24}, ${lastNode.dotX - 18} ${lastNode.dotY + 2}`
      : null,
  }
})

const vacancies = computed(() => fullResult.value?.vacancies ?? [])
const loadingMessage = computed(() => {
  const status = authJob.value?.jobStatus

  if (status === 'processing') {
    return `Нейросеть сейчас подготавливает персональные рекомендации${bestSpecialty.value !== 'результат теста' ? ` по направлению «${bestSpecialty.value}»` : ''}.`
  }

  return 'Собираем итог по результатам теста и данным профиля.'
})

function getDominantCategoryLabel(value) {
  if (!value) {
    return null
  }

  const normalizedValue = String(value).trim().toLowerCase()

  return DOMINANT_CATEGORY_LABELS[normalizedValue] ?? value
}

function buildPathBadges(step, limit = 2) {
  const badges = []

  if (step.experienceRequired && step.experienceRequired !== 'не указан') {
    badges.push(`Опыт: ${step.experienceRequired}`)
  }

  if (Array.isArray(step.skillsToLearn)) {
    badges.push(...step.skillsToLearn.filter(Boolean))
  }

  return badges.slice(0, limit)
}

function buildFallbackPathBadges(values) {
  return values
    .filter(Boolean)
    .map((value) => String(value).trim())
    .filter(Boolean)
    .slice(0, 2)
}

function normalizeCourses(value) {
  if (!Array.isArray(value)) {
    return []
  }

  return value
    .map((course) => ({
      id: course.stepik_course_id ?? course.url ?? course.title,
      title: course.title ?? 'Курс',
      summary: course.summary ?? 'Описание курса появится позже.',
      url: course.url ?? null,
      coverUrl: course.cover_url ?? null,
      skill: course.skill ?? null,
      isFree: course.is_free === true,
      price: course.price ?? null,
      currency: course.currency ?? null,
      durationHours: course.time_to_complete_hours ?? null,
      learnersCount: course.learners_count ?? null,
    }))
    .filter((course) => course.id && course.title)
}

function openPathCourses(step) {
  if (!step?.courses?.length) {
    return
  }

  selectedPathStep.value = step
}

function closePathCourses() {
  selectedPathStep.value = null
}

function handleCoursesWheel(event) {
  const rail = event.currentTarget

  if (!rail) {
    return
  }

  const horizontalDelta = Math.abs(event.deltaX) > Math.abs(event.deltaY)
    ? event.deltaX
    : event.deltaY

  rail.scrollBy({
    left: horizontalDelta,
    behavior: 'auto',
  })
}

function handleEscapeKey(event) {
  if (event.key === 'Escape' && selectedPathStep.value) {
    closePathCourses()
  }
}

function parseUserExperienceMonths(value) {
  if (!value) {
    return null
  }

  const normalizedValue = String(value).toLowerCase()

  if (normalizedValue.includes('без опыта')) {
    return 0
  }

  const yearMatch = normalizedValue.match(/(\d+)\s*(?:г\.|год|года|лет)/)
  const monthMatch = normalizedValue.match(/(\d+)\s*(?:мес\.|месяц|месяца|месяцев)/)

  const years = yearMatch ? Number(yearMatch[1]) : 0
  const months = monthMatch ? Number(monthMatch[1]) : 0
  const totalMonths = years * 12 + months

  return Number.isFinite(totalMonths) ? totalMonths : null
}

function parseExperienceRequirement(value) {
  if (!value) {
    return null
  }

  const normalizedValue = String(value).toLowerCase().replace(/[–—]/g, '-')

  if (normalizedValue.includes('без опыта')) {
    return { minMonths: 0, maxMonths: 0 }
  }

  const rangeMatch = normalizedValue.match(/(\d+)\s*-\s*(\d+)/)

  if (rangeMatch) {
    return {
      minMonths: Number(rangeMatch[1]) * 12,
      maxMonths: Number(rangeMatch[2]) * 12,
    }
  }

  const fromMatch = normalizedValue.match(/от\s*(\d+)/)

  if (fromMatch) {
    return {
      minMonths: Number(fromMatch[1]) * 12,
      maxMonths: null,
    }
  }

  const exactMatch = normalizedValue.match(/(\d+)/)

  if (exactMatch) {
    const months = Number(exactMatch[1]) * 12

    return {
      minMonths: months,
      maxMonths: months,
    }
  }

  return null
}

function findCurrentNodeIndex(nodes, months) {
  if (!Array.isArray(nodes) || !nodes.length || months == null) {
    return 0
  }

  let bestIndex = 0
  let bestMinMonths = -1

  for (let index = 1; index < nodes.length; index += 1) {
    const range = parseExperienceRequirement(nodes[index].experienceRequired)

    if (!range) {
      continue
    }

    const matchesMin = months >= range.minMonths
    const matchesMax = range.maxMonths == null || months <= range.maxMonths

    if (matchesMin && matchesMax && range.minMonths >= bestMinMonths) {
      bestIndex = index
      bestMinMonths = range.minMonths
    }
  }

  return bestIndex
}

const selectedPathCoursesHeading = computed(() => selectedPathStep.value?.title ?? 'Подходящие курсы')

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

function formatCoursePrice(course) {
  if (course.price == null) {
    return 'Цена уточняется'
  }

  return course.currency ? `${course.price} ${course.currency}` : String(course.price)
}

watch(selectedPathStep, (step) => {
  document.body.style.overflow = step ? 'hidden' : ''
})

onMounted(() => {
  mediaQueryList = window.matchMedia('(min-width: 768px) and (pointer: fine)')
  handleStorageChange()
  updateInteractivity()
  mediaQueryList.addEventListener('change', updateInteractivity)
  window.addEventListener('storage', handleStorageChange)
  window.addEventListener('keydown', handleEscapeKey)
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
  window.removeEventListener('keydown', handleEscapeKey)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.homepage-page {
  background: linear-gradient(135deg, #161455 0%, #21176e 34%, #4a1d67 62%, #241782 100%);
  color: #fff;
}

.homepage-hero {
  isolation: isolate;
}

.homepage-title {
  color: #ffd7eb;
}

.homepage-subtitle {
  color: #cac9ff;
}

.homepage-section-title {
  color: #fff3fa;
}

.homepage-section-text {
  color: rgba(255, 255, 255, 0.88);
}

.homepage-loading-panel,
.homepage-error-panel {
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(124, 120, 255, 0.12));
  box-shadow: 0 24px 64px rgba(9, 5, 40, 0.22);
  backdrop-filter: blur(18px);
}

.homepage-spinner {
  border-color: rgba(111, 127, 255, 0.24);
  border-top-color: #6f7fff;
}

.homepage-loading-kicker {
  color: rgba(255, 255, 255, 0.84);
}

.homepage-loading-text {
  color: rgba(255, 255, 255, 0.74);
}

.homepage-error-panel {
  color: #ffe6ef;
}

.homepage-profession-chip {
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  box-shadow: 0 18px 44px rgba(9, 5, 40, 0.16);
}

.homepage-cta {
  background: linear-gradient(180deg, #587bff 0%, #5065ff 100%);
  color: #fff;
  box-shadow: 0 14px 30px rgba(76, 91, 255, 0.35);
}

.homepage-cta:hover {
  background: linear-gradient(180deg, #6988ff 0%, #5d72ff 100%);
}

.homepage-vacancies-link {
  color: rgba(255, 255, 255, 0.92);
  font-weight: 600;
  line-height: 1.25;
}

.homepage-vacancies-link__anchor {
  color: #fff;
  text-decoration: underline;
  text-decoration-thickness: 2px;
  text-underline-offset: 0.16em;
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

.homepage-path {
  position: relative;
  overflow: visible;
}

.homepage-path__header {
  max-width: 46rem;
}

.homepage-path__title {
  margin: 0;
}

.homepage-path__summary {
  margin-top: 1rem;
  max-width: 34rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
}

.homepage-path__canvas {
  position: relative;
  min-height: 52rem;
  margin-top: 2.75rem;
}

.homepage-path__diagram {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
  fill: none;
  pointer-events: none;
}

.homepage-path__diagram-line {
  stroke: rgba(255, 255, 255, 0.92);
  stroke-linecap: round;
  stroke-width: 2.1;
}

.homepage-path__diagram-accent {
  stroke: #ff2c63;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 2.2;
  marker-end: url(#homepage-path-arrowhead);
}

.homepage-path__label {
  position: absolute;
  z-index: 2;
  color: #ff345f;
  font-size: clamp(1rem, 1.35vw, 1.55rem);
  font-weight: 900;
  line-height: 1.02;
  text-transform: uppercase;
}

.homepage-path__label--current {
  top: 2.8rem;
  left: 2.2rem;
}

.homepage-path__label--future {
  max-width: 15rem;
  text-align: center;
}

.homepage-path__mobile-label {
  display: none;
}

.homepage-path__node {
  position: absolute;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.85rem;
  width: min(18rem, 32%);
}

.homepage-path__node--interactive {
  cursor: pointer;
}

.homepage-path__node--interactive::after {
  content: '';
  position: absolute;
  inset: -0.75rem;
  border-radius: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0);
  background: rgba(255, 255, 255, 0);
  transition: border-color 0.2s ease, background-color 0.2s ease;
  z-index: -1;
}

.homepage-path__node--interactive:hover::after,
.homepage-path__node--interactive:focus-visible::after {
  border-color: rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
}

.homepage-path__node--interactive:hover .homepage-path__node-title,
.homepage-path__node--interactive:focus-visible .homepage-path__node-title {
  color: #ffd7eb;
}

.homepage-path__node--interactive:focus-visible {
  outline: none;
}

.homepage-path__node--left {
  left: 2.4rem;
}

.homepage-path__node--right {
  right: 2.4rem;
}

.homepage-path__dot {
  position: absolute;
  top: 0;
  width: 1rem;
  height: 1rem;
  border-radius: 9999px;
  background: #ff9db8;
  box-shadow: 0 0 0 7px rgba(255, 157, 184, 0.08);
}

.homepage-path__node--left .homepage-path__dot {
  right: 0.8rem;
}

.homepage-path__node--right .homepage-path__dot {
  left: 0.8rem;
}

.homepage-path__node-title {
  margin: 2.15rem 0 0;
  color: #fff;
  font-size: clamp(1.6rem, 2vw, 2.05rem);
  font-weight: 500;
  line-height: 1.08;
}

.homepage-path__hint {
  margin: 0.2rem 0 0;
  color: rgba(255, 215, 235, 0.84);
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.homepage-path__node--interactive:hover .homepage-path__hint,
.homepage-path__node--interactive:focus-visible .homepage-path__hint {
  color: #fff3fa;
}

.homepage-path__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
}

.homepage-path__chip {
  display: inline-flex;
  align-items: center;
  min-height: 2.05rem;
  border-radius: 9999px;
  background: #5d72ff;
  padding: 0.42rem 0.95rem;
  color: rgba(255, 255, 255, 0.95);
  font-size: 0.8rem;
  line-height: 1.2;
}

.homepage-modal {
  position: fixed;
  inset: 0;
  z-index: 80;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(11, 6, 37, 0.52);
  padding: 1.25rem;
  backdrop-filter: blur(10px);
}

.homepage-modal__panel {
  position: relative;
  width: min(100%, 68rem);
  max-height: min(88vh, 42rem);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 2rem;
  background: linear-gradient(180deg, rgba(237, 183, 255, 0.22), rgba(237, 183, 255, 0.12));
  box-shadow: 0 28px 80px rgba(9, 5, 40, 0.35);
  backdrop-filter: blur(28px);
  padding: 1.6rem 1.2rem 1.4rem;
}

.homepage-modal__close {
  position: absolute;
  top: 0.9rem;
  right: 1rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 9999px;
  color: rgba(255, 255, 255, 0.82);
  font-size: 1.75rem;
  line-height: 1;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.homepage-modal__close:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}

.homepage-modal__header {
  padding: 0 2.5rem 0 0.4rem;
}

.homepage-modal__kicker {
  margin: 0;
  color: rgba(255, 255, 255, 0.72);
  font-size: 0.84rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.homepage-modal__title {
  margin: 0.6rem 0 0;
  color: #fff3fa;
  font-size: clamp(1.7rem, 3vw, 2.6rem);
  font-weight: 900;
  line-height: 1.02;
}

.homepage-modal__rail {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  overflow-y: hidden;
  margin-top: 1.6rem;
  padding: 0.3rem 0.35rem 0.6rem;
  scroll-snap-type: x proximity;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.28) transparent;
  overscroll-behavior-x: contain;
}

.homepage-course-card {
  flex: 0 0 min(20rem, calc(100vw - 4rem));
  display: flex;
  flex-direction: column;
  min-height: 0;
  max-height: 33rem;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 1.5rem;
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 20px 44px rgba(9, 5, 40, 0.18);
  overflow: hidden;
  scroll-snap-align: start;
}

.homepage-course-card__cover {
  aspect-ratio: 16 / 8.5;
  background: rgba(255, 255, 255, 0.08);
  flex: 0 0 auto;
}

.homepage-course-card__cover-image {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.homepage-course-card__body {
  display: flex;
  flex: 1;
  flex-direction: column;
  padding: 1rem;
  min-height: 0;
}

.homepage-course-card__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.homepage-course-card__chip {
  display: inline-flex;
  align-items: center;
  min-height: 1.85rem;
  border-radius: 9999px;
  background: rgba(93, 114, 255, 0.92);
  padding: 0.32rem 0.8rem;
  color: rgba(255, 255, 255, 0.95);
  font-size: 0.76rem;
  line-height: 1.15;
}

.homepage-course-card__title {
  margin: 0.95rem 0 0;
  color: #fff;
  font-size: 1.15rem;
  font-weight: 800;
  line-height: 1.2;
  text-decoration: none;
}

a.homepage-course-card__title:hover {
  color: #ffd7eb;
}

.homepage-course-card__summary {
  margin: 0.8rem 0 0;
  color: rgba(255, 255, 255, 0.82);
  font-size: 0.92rem;
  line-height: 1.45;
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
}

.homepage-course-card__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  margin-top: auto;
  padding-top: 1rem;
  color: rgba(255, 255, 255, 0.66);
  font-size: 0.8rem;
}

@media (max-width: 1023px) {
  .homepage-path__canvas {
    min-height: 50rem;
  }

  .homepage-path__label--future {
    max-width: 13rem;
  }

  .homepage-path__node {
    width: min(19rem, 36%);
  }

  .homepage-modal__panel {
    width: min(100%, 58rem);
  }
}

@media (max-width: 767px), (pointer: coarse) {
  .homepage-hero__background {
    width: min(135vw, 820px);
    opacity: 0.82;
    transform: translate3d(-50%, -44%, 0);
  }

  .homepage-path__summary {
    max-width: none;
  }

  .homepage-path__canvas {
    min-height: auto;
    display: flex;
    flex-direction: column;
    gap: 1.8rem;
    margin-top: 2rem;
    padding-top: 0.2rem;
  }

  .homepage-path__diagram {
    display: none;
  }

  .homepage-path__label {
    display: none;
  }

  .homepage-path__label,
  .homepage-path__node {
    position: static;
  }

  .homepage-path__mobile-label {
    display: block;
    margin-bottom: 0.75rem;
    color: #ff345f;
    font-size: 0.9rem;
    font-weight: 900;
    line-height: 0.96;
    text-transform: uppercase;
  }

  .homepage-path__node {
    gap: 0.7rem;
    max-width: none;
    width: auto;
    padding-left: 0;
  }

  .homepage-path__dot {
    display: none;
  }

  .homepage-path__node-title {
    margin-top: 0;
    font-size: 1.35rem;
  }

  .homepage-path__chip {
    font-size: 0.76rem;
  }

  .homepage-modal {
    align-items: stretch;
    padding: 0;
  }

  .homepage-modal__panel {
    width: 100%;
    height: 100dvh;
    max-height: 100dvh;
    border-radius: 0;
    padding: 0.85rem 0.7rem 0.85rem;
  }

  .homepage-modal__header {
    padding-right: 2.6rem;
  }

  .homepage-modal__kicker {
    font-size: 0.68rem;
  }

  .homepage-modal__title {
    font-size: 1.2rem;
    line-height: 1.08;
  }

  .homepage-modal__rail {
    margin-top: 1rem;
    height: calc(100dvh - 6.2rem);
    padding: 0.1rem 0.05rem 0.5rem;
    align-items: stretch;
  }

  .homepage-course-card {
    flex: 0 0 calc(100vw - 1.5rem);
    width: calc(100vw - 1.5rem);
    max-width: calc(100vw - 1.5rem);
    height: 100%;
    max-height: none;
    border-radius: 1.2rem;
  }

  .homepage-course-card__cover {
    aspect-ratio: 16 / 3.6;
  }

  .homepage-course-card__title {
    margin-top: 0.75rem;
    font-size: 0.92rem;
  }

  .homepage-course-card__summary {
    margin-top: 0.55rem;
    font-size: 0.76rem;
    line-height: 1.35;
    -webkit-line-clamp: 5;
    text-overflow: ellipsis;
  }

  .homepage-course-card__body {
    padding: 0.75rem;
    flex: 1;
    min-height: 0;
  }

  .homepage-course-card__chip {
    min-height: 1.65rem;
    padding: 0.28rem 0.68rem;
    font-size: 0.68rem;
  }

  .homepage-course-card__meta {
    gap: 0.55rem;
    padding-top: 0.7rem;
    font-size: 0.72rem;
  }

  .homepage-modal__close {
    top: 0.65rem;
    right: 0.7rem;
    width: 2.2rem;
    height: 2.2rem;
    font-size: 1.55rem;
  }
}
</style>
