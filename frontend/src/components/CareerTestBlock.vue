<template>
  <section class="career-test-block relative w-full overflow-hidden py-4 sm:py-6 lg:py-8">
    <div class="relative z-10 text-center">
      <h2 class="career-test-block__title">
        Тест по определению<br class="hidden lg:block"> направления
      </h2>
    </div>

    <div class="career-test-stage relative z-10 mt-6 sm:mt-8">
      <div class="career-test-track px-4 sm:px-8 lg:px-12">
        <div class="career-test-main relative mx-auto flex w-full items-center justify-center">
          <div class="career-test-card-shell w-full">
            <Transition :name="transitionName" :css="!isMobileView">
              <article
                :key="isCompletedView ? 'completed' : currentQuestion.id"
                class="career-test-card w-full rounded-4xl px-6 py-7 sm:min-h-96 sm:px-10 sm:py-8 lg:h-100min-h-[25rem]"
              >
                <template v-if="!isCompletedView">
                  <div class="career-test-card__heading">
                    <p class="career-test-card__meta">Вопрос {{ currentQuestionIndex + 1 }}</p>
                    <h3 class="career-test-card__title">{{ currentQuestion.title }}:</h3>
                  </div>

                  <div class="mt-4 space-y-3 sm:mt-5 sm:space-y-4">
                    <button
                      v-for="option in currentQuestion.options"
                      :key="option.key"
                      type="button"
                      class="career-test-option"
                      :class="selectedOptionClass(currentQuestion.id, option.key)"
                      @click="handleOptionSelect(currentQuestion.id, option.key)"
                    >
                      {{ capitalize(option.label) }}.
                    </button>
                  </div>
                </template>

                <template v-else>
                  <div class="flex min-h-72 flex-col items-center justify-center text-center sm:min-h-80 lg:min-h-112">
                    <p class="career-test-card__meta">Готово</p>
                    <h3 class="career-test-card__title">Тест завершен</h3>
                    <p class="mt-4 max-w-xl text-sm leading-6 text-white/72 sm:text-base">
                      Мы сохранили ответы и продолжили дальнейшую логику обработки.
                    </p>
                  </div>
                </template>
              </article>
            </Transition>
          </div>
        </div>

        <div v-if="!isCompletedView" class="career-test-controls">
          <button
            type="button"
            class="career-test-arrow career-test-arrow--left"
            :disabled="!canGoBack"
            @click="goBack"
          >
            <svg viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="m15 5-7 7 7 7" />
            </svg>
          </button>

          <button
            type="button"
            class="career-test-arrow career-test-arrow--right"
            :disabled="!canGoForward"
            @click="goForward"
          >
            <svg viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="m9 5 7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div class="career-test-progress relative z-10">
      <span
        v-for="question in questions"
        :key="question.id"
        class="h-2.5 rounded-full transition-all duration-300"
        :class="answers[question.id] || currentQuestion.id === question.id ? 'w-2.5 bg-white/90' : 'w-2.5 bg-white/20'"
      />
    </div>

    <div
      v-if="submitError"
      class="relative z-10 mx-auto mt-6 max-w-3xl rounded-2xl border border-rose-300/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-100"
    >
      {{ submitError }}
    </div>

    <div
      v-if="isLoadingResults"
      class="absolute inset-0 z-30 flex items-center justify-center bg-[#1b165f]/58 backdrop-blur-sm"
    >
      <div class="rounded-3xl border border-white/12 bg-white/10 px-6 py-6 text-center shadow-[0_24px_70px_rgba(15,8,54,0.4)] backdrop-blur-xl">
        <div class="mx-auto h-10 w-10 animate-spin rounded-full border-3 border-white/20 border-t-white" />
        <p class="mt-4 text-xs font-semibold uppercase tracking-[0.22em] text-white/78">
          Анализируем ответы
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'

import { CAREER_TEST_COLUMNS, CAREER_TEST_QUESTIONS } from '@/constants/careerTest'
import { submitAnonymousTest } from '@/lib/api'
import {
  STORAGE_KEYS,
  mapScoreArrayToApiScores,
  writeStorageJson,
  writeStorageValue,
} from '@/lib/storage'

const questions = CAREER_TEST_QUESTIONS
const answers = reactive({})
const currentQuestionIndex = ref(0)
const isLoadingResults = ref(false)
const isCompletedView = ref(false)
const submitError = ref('')
const transitionName = ref('question-slide-forward')
const isMobileView = ref(false)

const currentQuestion = computed(() => questions[currentQuestionIndex.value])
const canGoBack = computed(() => currentQuestionIndex.value > 0 && !isLoadingResults.value)
const canGoForward = computed(() => Boolean(answers[currentQuestion.value.id]) && !isLoadingResults.value)

const scoredColumns = computed(() => {
  const totals = Object.fromEntries(CAREER_TEST_COLUMNS.map((column) => [column.id, 0]))

  for (const question of questions) {
    const selectedKey = answers[question.id]
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

let mediaQuery = null

function syncMobileView() {
  isMobileView.value = window.matchMedia('(max-width: 767px)').matches
}

onMounted(() => {
  mediaQuery = window.matchMedia('(max-width: 767px)')
  syncMobileView()
  mediaQuery.addEventListener('change', syncMobileView)
})

onBeforeUnmount(() => {
  mediaQuery?.removeEventListener('change', syncMobileView)
})

function persistScores(scoreValues) {
  writeStorageJson(STORAGE_KEYS.testScores, scoreValues)
}

function persistPreview(preview) {
  writeStorageJson(STORAGE_KEYS.testPreview, preview)
  writeStorageValue(STORAGE_KEYS.attemptToken, preview.attempt_token)
}

async function submitResults() {
  const values = scoredColumns.value.map((column) => column.score)
  persistScores(values)
  submitError.value = ''

  const preview = await submitAnonymousTest(mapScoreArrayToApiScores(values))
  persistPreview(preview)
}

function selectedOptionClass(questionId, optionKey) {
  return answers[questionId] === optionKey
    ? 'career-test-option--selected'
    : 'career-test-option--idle'
}

function capitalize(value) {
  if (!value) {
    return ''
  }

  return value.charAt(0).toUpperCase() + value.slice(1)
}

function goBack() {
  if (!canGoBack.value) {
    return
  }

  transitionName.value = 'question-slide-backward'
  currentQuestionIndex.value -= 1
}

async function goForward() {
  if (!canGoForward.value) {
    return
  }

  if (currentQuestionIndex.value === questions.length - 1) {
    isLoadingResults.value = true

    try {
      await submitResults()
      isCompletedView.value = true
    } catch (error) {
      submitError.value = error?.message ?? 'Не удалось получить результат теста.'
    } finally {
      isLoadingResults.value = false
    }

    return
  }

  transitionName.value = 'question-slide-forward'
  currentQuestionIndex.value += 1
}

async function handleOptionSelect(questionId, optionKey) {
  if (isLoadingResults.value) {
    return
  }

  answers[questionId] = optionKey
  await new Promise((resolve) => window.setTimeout(resolve, 180))

  if (currentQuestion.value.id !== questionId) {
    return
  }

  await goForward()
}
</script>

<style scoped>
.career-test-block {
  min-height: 42rem;
}

.career-test-block__title {
  color: #fff;
  font-size: clamp(2.6rem, 6vw, 4.6rem);
  font-weight: 900;
  line-height: 1.08;
  text-transform: uppercase;
  text-shadow: 0 12px 48px rgba(4, 2, 38, 0.26);
}

.career-test-stage {
  min-height: 29rem;
  overflow: hidden;
}

.career-test-track {
  position: relative;
  min-height: 25rem;
}

.career-test-main {
  max-width: 58rem;
  min-height: 25rem;
}

.career-test-card {
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: linear-gradient(180deg, rgba(183, 146, 255, 0.38), rgba(141, 115, 210, 0.3));
  box-shadow: 0 28px 40px rgba(12, 8, 50, 0.35);
  backdrop-filter: blur(24px);
}

.career-test-card-shell {
  position: relative;
  min-height: 25rem;
  overflow: visible;
  isolation: isolate;
}

.career-test-card__heading {
  min-height: 7.2rem;
}

.career-test-card__meta {
  color: rgba(255, 255, 255, 0.84);
  font-size: 0.95rem;
  line-height: 1.4;
}

.career-test-card__title {
  margin-top: 1.2rem;
  color: #fff;
  font-size: clamp(1.7rem, 2.6vw, 2.35rem);
  font-weight: 800;
  line-height: 1.15;
}

.career-test-option {
  display: flex;
  width: 100%;
  border-radius: 1.15rem;
  padding: 1rem 1.15rem;
  text-align: left;
  color: #fff;
  font-size: clamp(1rem, 1.2vw, 1.25rem);
  line-height: 1.4;
  transition: background-color 0.25s ease, transform 0.25s ease, border-color 0.25s ease;
}

.career-test-option--idle {
  border: 1px solid transparent;
  background: transparent;
}

.career-test-option--idle:hover {
  background: rgba(255, 255, 255, 0.05);
}

.career-test-option--selected {
  border: 1px solid rgba(255, 255, 255, 0.04);
  background: rgba(204, 181, 255, 0.24);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.04);
}

.career-test-arrow {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 3.2rem;
  height: 3.2rem;
  border-radius: 9999px;
  background: rgba(211, 162, 255, 0.26);
  color: #f3d0ff;
  box-shadow: 0 20px 40px rgba(24, 12, 70, 0.22);
  backdrop-filter: blur(18px);
  transition: transform 0.2s ease, opacity 0.2s ease, background-color 0.2s ease;
}

.career-test-controls {
  pointer-events: none;
}

.career-test-progress {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
}

.career-test-arrow:hover:not(:disabled) {
  background: rgba(221, 173, 255, 0.32);
}

.career-test-arrow:disabled {
  cursor: not-allowed;
  opacity: 0.34;
}

.question-slide-forward-enter-active,
.question-slide-forward-leave-active,
.question-slide-backward-enter-active,
.question-slide-backward-leave-active {
  position: absolute;
  inset: 0;
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.3s ease;
  backface-visibility: hidden;
  will-change: transform, opacity;
}

.question-slide-forward-enter-from {
  opacity: 0.18;
  transform: translateX(100vw);
}

.question-slide-forward-leave-to {
  transform: translateX(-100vw);
}

.question-slide-backward-enter-from {
  opacity: 0.18;
  transform: translateX(-100vw);
}

.question-slide-backward-leave-to {
  transform: translateX(100vw);
}

.question-slide-forward-enter-to,
.question-slide-backward-enter-to,
.question-slide-forward-leave-from,
.question-slide-backward-leave-from {
  opacity: 1;
  transform: translateX(0);
}

.question-slide-forward-leave-active,
.question-slide-backward-leave-active {
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

@media (max-width: 1279px) {
  .career-test-block {
    min-height: auto;
  }
}

@media (min-width: 768px) {
  .career-test-controls {
    position: absolute;
    top: 0;
    left: 50%;
    width: min(calc(100% - 2rem), 58rem);
    height: 25rem;
    transform: translateX(-50%);
    pointer-events: none;
  }

  .career-test-controls .career-test-arrow {
    position: absolute;
    top: 50%;
    pointer-events: auto;
    transform: translateY(-50%);
    z-index: 3;
  }

  .career-test-controls .career-test-arrow--left {
    left: -3.5rem;
  }

  .career-test-controls .career-test-arrow--right {
    right: -3.5rem;
  }
}

@media (max-width: 767px) {
  .career-test-block__title {
    font-size: 2rem;
  }

  .career-test-stage {
    min-height: 25rem;
  }

  .career-test-track,
  .career-test-main {
    min-height: 22rem;
  }

  .career-test-card {
    min-height: 22rem;
    padding-left: 1.25rem;
    padding-right: 1.25rem;
  }

  .career-test-card-shell {
    min-height: 22rem;
    overflow: visible;
    isolation: auto;
  }

  .career-test-card__heading {
    min-height: 6.4rem;
  }

  .career-test-card__title {
    font-size: 1.6rem;
  }

  .career-test-option {
    font-size: 0.95rem;
  }

  .career-test-arrow {
    width: 2.8rem;
    height: 2.8rem;
  }

  .career-test-controls {
    display: flex;
    justify-content: center;
    gap: 0.85rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
    pointer-events: auto;
  }

  .career-test-controls .career-test-arrow {
    position: static;
  }

  .career-test-progress {
    display: grid;
    grid-template-columns: repeat(12, minmax(0, 1fr));
    justify-content: center;
    gap: 0.55rem 0.45rem;
    width: fit-content;
    max-width: 100%;
    margin: 0 auto;
  }
}
</style>
