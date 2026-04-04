<template>
  <div
    class="flex flex-col bg-(--page-bg-alt) transition-colors duration-300"
    :class="isSummaryVisible ? 'min-h-screen overflow-visible' : 'h-screen overflow-hidden'"
  >
    <SiteHeader />

    <main
      class="flex flex-1"
      :class="isSummaryVisible ? 'min-h-0 overflow-visible' : 'min-h-0 overflow-hidden'"
    >
      <section
        class="flex flex-1 px-0 py-4 sm:px-4 sm:py-5 lg:px-8"
        :class="isSummaryVisible ? 'min-h-0 items-start pb-8 sm:pb-10' : 'min-h-0 overflow-hidden'"
      >
        <div class="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-4 px-4 sm:px-6 lg:px-8">
          <div class="max-w-5xl shrink-0">
            <h1
              class="mt-2 text-3xl font-black uppercase leading-[0.95] tracking-[-0.04em] text-(--text-hero) sm:text-5xl"
            >
              Тест по определению направления
            </h1>
            <p v-if="!isSummaryVisible" class="mt-3 max-w-2xl text-sm leading-6 text-(--text-accent-soft) sm:text-base">
              Время прохождения 2-5 минут
            </p>
          </div>

          <div
            v-if="!isSummaryVisible"
            class="relative flex min-h-0 flex-1 flex-col overflow-hidden rounded-4xl bg-(--surface) p-4 shadow-(--shadow-card) sm:p-6"
          >
            <div ref="timelineContainerRef" class="timeline-scrollbar-hidden shrink-0 overflow-x-auto pb-2">
              <div class="mx-auto flex min-w-max items-center justify-center">
                <template v-for="(question, index) in questions" :key="question.id">
                  <div
                    :ref="(element) => setTimelineItemRef(question.id, element)"
                    class="flex min-w-10 flex-col items-center text-center sm:min-w-12"
                  >
                    <div
                      class="flex h-9 w-9 items-center justify-center rounded-full border-2 text-xs font-bold transition sm:h-11 sm:w-11 sm:text-sm"
                      :class="timelineCircleClass(index)"
                    >
                      <svg
                        v-if="isQuestionConfirmed(index)"
                        viewBox="0 0 24 24"
                        class="h-4 w-4"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="3"
                      >
                        <path d="m5 13 4 4L19 7" />
                      </svg>
                      <span v-else>{{ index + 1 }}</span>
                    </div>
                  </div>

                  <div
                    v-if="index < questions.length - 1"
                    class="mx-1.5 h-1 w-6 rounded-full sm:mx-2 sm:w-14"
                    :class="isQuestionConfirmed(index) ? 'bg-emerald-500' : 'bg-(--surface-soft)'"
                  />
                </template>
              </div>
            </div>

            <div class="mt-4 min-h-0 flex-1 space-y-4 overflow-y-auto pb-8 pr-1 sm:pb-4">
              <article
                v-for="(question, index) in visibleQuestions"
                :key="question.id"
                :ref="(element) => setQuestionRef(question.id, element)"
                tabindex="0"
                class="rounded-3xl border border-(--border-soft) bg-(--surface-soft-2) p-4 sm:p-5"
                @keydown.enter.prevent="handleQuestionEnter(question.id, index)"
              >
                <div class="flex items-start justify-between gap-4">
                  <div>
                    <p class="text-xs font-semibold uppercase tracking-[0.2em] text-(--text-muted)">
                      Вопрос {{ index + 1 }}
                    </p>
                    <h2 class="mt-2 text-lg font-bold leading-snug text-(--text-hero) sm:text-xl">
                      {{ question.title }}
                    </h2>
                  </div>

                  <div
                    v-if="isQuestionConfirmed(index)"
                    class="mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-emerald-500 text-white"
                  >
                    <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="3">
                      <path d="m5 13 4 4L19 7" />
                    </svg>
                  </div>
                </div>

                <div v-if="isQuestionConfirmed(index)" class="mt-4">
                  <p class="text-sm font-medium text-(--text-main)/65">Ваш ответ</p>
                  <div
                    class="mt-3 inline-flex rounded-2xl bg-emerald-500/14 px-4 py-3 text-sm font-semibold leading-6 text-emerald-700 transition dark:text-emerald-300"
                  >
                    {{ getConfirmedOptionLabel(question.id) }}
                  </div>
                </div>

                <div v-else class="mt-5">
                  <div class="grid gap-2.5">
                    <button
                      v-for="option in question.options"
                      :key="option.key"
                      type="button"
                      class="rounded-2xl border px-4 py-3 text-left text-sm leading-6 transition sm:text-base"
                      :class="selectedOptionClass(question.id, option.key)"
                      @click="selectAnswer(question.id, option.key)"
                    >
                      <span class="font-semibold text-(--text-hero)">{{ option.prefix }})</span>
                      {{ ' ' }}{{ option.label }}
                    </button>
                  </div>

                  <div class="mt-4 flex justify-end">
                    <button
                      type="button"
                      class="inline-flex min-h-11 items-center justify-center rounded-full px-6 text-sm font-bold uppercase tracking-[0.12em] text-(--button-text) shadow-[0_8px_18px_rgba(29,16,126,0.18)] transition"
                      :class="draftAnswers[question.id] ? 'bg-(--button-secondary) hover:bg-(--button-secondary-hover)' : 'cursor-not-allowed bg-(--text-muted)/45 shadow-none'"
                      :disabled="!draftAnswers[question.id]"
                      @click="confirmAnswer(question.id)"
                    >
                      Подтвердить
                    </button>
                  </div>
                </div>
              </article>
            </div>

            <div
              v-if="isLoadingResults"
              class="absolute inset-0 z-10 flex items-center justify-center bg-(--surface)/55 backdrop-blur-sm"
            >
              <div class="rounded-3xl bg-(--surface)/92 px-6 py-6 text-center shadow-(--shadow-card)">
                <div class="mx-auto h-10 w-10 animate-spin rounded-full border-3 border-(--button-secondary)/20 border-t-(--button-secondary)" />
                <p class="mt-4 text-xs font-semibold uppercase tracking-[0.22em] text-(--text-accent-soft)">
                  Анализируем ответы
                </p>
              </div>
            </div>
          </div>

          <section
            v-if="isSummaryVisible"
            class="flex flex-col"
          >
            <div class="max-w-3xl shrink-0">
              <p class="text-sm font-semibold uppercase tracking-[0.24em] text-(--text-accent-soft)">
                Ваш результат
              </p>
            </div>

            <div class="mt-4 grid gap-4 sm:grid-cols-2">
              <article class="rounded-3xl bg-(--surface) p-4 shadow-(--shadow-card) sm:p-5">
                <h3 class="text-lg font-bold text-(--text-hero) sm:text-xl">О вас</h3>
                <p class="mt-3 text-sm leading-6 text-(--text-main)/80 sm:text-base">
                  {{ summary.about }}
                </p>
              </article>

              <article class="rounded-3xl bg-(--surface) p-4 shadow-(--shadow-card) sm:p-5">
                <h3 class="text-lg font-bold text-(--text-hero) sm:text-xl">
                  Проф. склонности, подходящие направления
                </h3>
                <p class="mt-3 text-sm leading-6 text-(--text-main)/80 sm:text-base">
                  {{ summary.directions }}
                </p>
              </article>

              <div class="relative overflow-hidden rounded-3xl sm:col-span-2">
                <img
                  :src="careerLockedPreview"
                  alt="Превью закрытого персонального плана и списка вакансий"
                  class="block w-full h-auto"
                />

                <div class="absolute inset-0 flex items-center justify-center p-4 sm:p-6">
                  <div class="w-full max-w-xl rounded-[1.1rem] bg-(--surface)/94 px-3 py-3 text-center shadow-(--shadow-card) sm:rounded-3xl sm:px-6 sm:py-5">
                    <p class="text-[10px] font-semibold uppercase tracking-[0.18em] text-(--text-accent-soft) sm:text-sm sm:tracking-[0.22em]">
                      Откройте полный доступ бесплатно
                    </p>
                    <h3 class="mt-1.5 text-[13px] font-black uppercase leading-[0.9] tracking-[-0.03em] text-(--text-hero) sm:mt-3 sm:text-2xl">
                      Зарегистрируйтесь, чтобы увидеть детали
                    </h3>
                    <p class="mt-2 hidden text-[11px] leading-4 text-(--text-main)/75 sm:block sm:text-base sm:leading-6">
                      После регистрации откроем персональный план развития, полный список вакансий и детальный разбор ваших сильных сторон.
                    </p>
                    <RouterLink
                      to="/auth"
                      class="mt-2.5 inline-flex min-h-8 items-center justify-center rounded-full bg-(--button-secondary) px-4 text-[11px] font-bold uppercase tracking-[0.12em] text-(--button-text) transition hover:bg-(--button-secondary-hover) sm:mt-4 sm:min-h-11 sm:px-6 sm:text-sm"
                      style="color: var(--button-text)"
                    >
                      Регистрация
                    </RouterLink>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'

import careerLockedPreviewDark from '@/assets/career-locked-preview-dark.png'
import careerLockedPreviewLight from '@/assets/career-locked-preview-light.png'
import SiteHeader from '@/components/ThemedSiteHeader.vue'
import {
  CAREER_TEST_COLUMNS,
  CAREER_TEST_QUESTIONS,
  CAREER_TEST_SUMMARY,
} from '@/constants/careerTest'
import { useTheme } from '@/composables/useTheme'

const questions = CAREER_TEST_QUESTIONS
const summary = CAREER_TEST_SUMMARY
const RESULTS_STORAGE_KEY = 'career-ai-test-results'
const { isDark } = useTheme()

const draftAnswers = reactive({})
const confirmedAnswers = reactive({})
const questionRefs = ref({})
const timelineItemRefs = ref({})
const timelineContainerRef = ref(null)
const isLoadingResults = ref(false)
let resultsTimeoutId = null

const completedCount = computed(() => Object.keys(confirmedAnswers).length)
const visibleQuestionCount = computed(() => Math.min(completedCount.value + 1, questions.length))
const visibleQuestions = computed(() => questions.slice(0, visibleQuestionCount.value))
const isCompleted = computed(() => completedCount.value === questions.length)
const isSummaryVisible = computed(() => isCompleted.value && !isLoadingResults.value)
const careerLockedPreview = computed(() =>
  isDark.value ? careerLockedPreviewDark : careerLockedPreviewLight,
)

const scoredColumns = computed(() => {
  const totals = Object.fromEntries(CAREER_TEST_COLUMNS.map((column) => [column.id, 0]))

  for (const question of questions) {
    const selectedKey = confirmedAnswers[question.id]
    const selectedOption = question.options.find((option) => option.key === selectedKey)

    if (selectedOption) {
      totals[selectedOption.column] += 1
    }
  }

  return CAREER_TEST_COLUMNS.map((column) => ({
    ...column,
    score: totals[column.id],
  }))
})

function persistResults() {
  if (typeof window === 'undefined') {
    return
  }

  const values = scoredColumns.value.map((column) => column.score)
  window.localStorage.setItem(RESULTS_STORAGE_KEY, JSON.stringify(values))
}

function selectAnswer(questionId, optionKey) {
  draftAnswers[questionId] = optionKey
}

async function confirmAnswer(questionId) {
  if (!draftAnswers[questionId]) {
    return
  }

  confirmedAnswers[questionId] = draftAnswers[questionId]

  if (Object.keys(confirmedAnswers).length === questions.length) {
    persistResults()
    isLoadingResults.value = true

    if (resultsTimeoutId) {
      clearTimeout(resultsTimeoutId)
    }

    resultsTimeoutId = setTimeout(() => {
      isLoadingResults.value = false
      resultsTimeoutId = null
    }, 1200)

    return
  }

  await nextTick()

  const currentIndex = questions.findIndex((question) => question.id === questionId)
  const nextQuestion = questions[currentIndex + 1]

  if (nextQuestion) {
    centerTimelineOnQuestion(nextQuestion.id)
    questionRefs.value[nextQuestion.id]?.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    })
  }
}

function isQuestionConfirmed(index) {
  return Boolean(confirmedAnswers[questions[index].id])
}

function getConfirmedOptionLabel(questionId) {
  const question = questions.find((item) => item.id === questionId)
  const selectedKey = confirmedAnswers[questionId]
  const option = question?.options.find((item) => item.key === selectedKey)

  return option ? `${option.prefix}) ${option.label}` : ''
}

function timelineCircleClass(index) {
  if (isQuestionConfirmed(index)) {
    return 'border-emerald-500 bg-emerald-500 text-white'
  }

  if (index === completedCount.value) {
    return 'border-(--button-secondary) bg-(--button-secondary)/10 text-(--button-secondary)'
  }

  return 'border-(--border-soft) bg-(--surface-soft) text-(--text-muted)'
}

function selectedOptionClass(questionId, optionKey) {
  return draftAnswers[questionId] === optionKey
    ? 'border-(--button-secondary) bg-(--button-secondary)/10 text-(--text-hero)'
    : 'border-(--border-soft) bg-(--surface) text-(--text-main) hover:border-(--button-secondary)/50 hover:bg-(--surface-soft)'
}

function setQuestionRef(questionId, element) {
  if (element) {
    questionRefs.value[questionId] = element
    return
  }

  delete questionRefs.value[questionId]
}

function setTimelineItemRef(questionId, element) {
  if (element) {
    timelineItemRefs.value[questionId] = element
    return
  }

  delete timelineItemRefs.value[questionId]
}

function centerTimelineOnQuestion(questionId) {
  const container = timelineContainerRef.value
  const item = timelineItemRefs.value[questionId]

  if (!container || !item) {
    return
  }

  const targetLeft = item.offsetLeft - container.clientWidth / 2 + item.clientWidth / 2

  container.scrollTo({
    left: Math.max(targetLeft, 0),
    behavior: 'smooth',
  })
}

function handleQuestionEnter(questionId, index) {
  if (isQuestionConfirmed(index) || !draftAnswers[questionId]) {
    return
  }

  confirmAnswer(questionId)
}

onBeforeUnmount(() => {
  if (resultsTimeoutId) {
    clearTimeout(resultsTimeoutId)
  }
})
</script>

<style scoped>
.timeline-scrollbar-hidden {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.timeline-scrollbar-hidden::-webkit-scrollbar {
  display: none;
}
</style>
