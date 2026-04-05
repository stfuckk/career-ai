<template>
  <div class="auth-page flex flex-col overflow-hidden">
    <div class="auth-page__background-object" :style="authBackgroundObjectStyle" aria-hidden="true" />
    <SiteHeader />

    <main class="relative z-10 flex flex-1 flex-col px-4 pb-8 pt-28 sm:px-8 sm:pt-32 lg:px-12 lg:pb-12 lg:pt-36">
      <div
        v-if="!previewResult"
        class="relative left-1/2 w-screen max-w-none -translate-x-1/2 overflow-hidden"
      >
        <CareerTestBlock />
      </div>

      <div
        v-if="pendingRegistration && !previewResult"
        class="mx-auto mt-6 w-full max-w-4xl rounded-3xl border border-white/12 bg-white/6 px-5 py-4 text-center text-sm leading-6 text-white/88 sm:text-base"
      >
        Данные для регистрации сохранены. Чтобы получить персональный анализ, пройдите тест выше.
      </div>

      <section
        v-if="previewResult"
        class="auth-preview mx-auto mt-14 w-full max-w-6xl px-2 sm:mt-18 sm:px-0"
      >
        <div class="auth-preview__surface">
          <div class="auth-preview__intro">
            <h2 class="auth-preview__title">
              Тест по определению
              направления
            </h2>
          </div>

          <div class="auth-preview__content">
            <article class="auth-preview__feature auth-preview__feature--left">
              <div class="auth-preview__copy">
                <h3 class="auth-preview__heading">Ваши качества</h3>
                <p class="auth-preview__text">
                  {{ previewQualitiesText }}
                </p>
              </div>
              <div class="auth-preview__art auth-preview__art--camera" aria-hidden="true">
                <img :src="cameraImage" alt="" class="auth-preview__art-image">
              </div>
            </article>

            <article class="auth-preview__feature auth-preview__feature--right">
              <div class="auth-preview__art auth-preview__art--paint" aria-hidden="true">
                <img :src="paintKitImage" alt="" class="auth-preview__art-image">
              </div>
              <div class="auth-preview__copy">
                <h3 class="auth-preview__heading">Профессиональные склонности</h3>
                <p class="auth-preview__text">
                  {{ previewCareerFitText }}
                </p>
              </div>
            </article>
          </div>

          <section class="auth-preview__locked" aria-label="Скрытая часть результата">
            <div class="auth-preview__locked-text">
              <p
                v-for="(paragraph, index) in lockedPreviewParagraphs"
                :key="`${paragraph}-${index}`"
                class="auth-preview__locked-paragraph"
              >
                {{ paragraph }}
              </p>
            </div>

            <div class="auth-preview__overlay">
              <p class="auth-preview__overlay-kicker">Откройте полный доступ</p>
              <h3 class="auth-preview__overlay-title">
                Зарегистрируйтесь, чтобы увидеть детали
              </h3>
              <p class="auth-preview__overlay-text">
                После регистрации откроем персональный план развития, полный список вакансий и детальный разбор ваших сильных сторон.
              </p>
              <button
                type="button"
                class="auth-preview__overlay-button"
                @click="scrollToAuthBlock"
              >
                Регистрация
              </button>
            </div>
          </section>
        </div>
      </section>

      <section class="mx-auto mt-20 grid w-full max-w-6xl items-center gap-10 lg:grid-cols-[0.95fr_1.05fr] lg:gap-14">
        <div class="auth-copy relative z-20 max-w-xl">
          <h1 class="auth-copy__title">
            {{ isLogin ? 'Вход в аккаунт' : 'Создание аккаунта' }}
          </h1>
          <p class="auth-copy__subtitle">
            {{ isLogin
              ? 'Войдите, чтобы продолжить работу с персональным карьерным планом и подборкой вакансий.'
              : 'Получите персональный план вашей карьеры бесплатно' }}
          </p>
        </div>

        <div id="auth-panel" class="auth-stage">

          <div
            class="auth-stage__floating auth-stage__floating--coin absolute z-10 -left-12 -top-6 md:-left-12 md:-top-4 lg:-left-40 lg:-top-5"
            aria-hidden="true"
          >
            <img
              :src="authFloatingCoin"
              alt=""
              class="auth-stage__image block w-64 max-w-none md:w-80 lg:w-120"
            >
          </div>

          <div
            class="auth-stage__floating auth-stage__floating--briefcase absolute z-10 -right-10 bottom-0 md:-right-10 md:top-26 md:bottom-auto lg:-right-44 lg:top-13"
            aria-hidden="true"
          >
            <img
              :src="authFloatingBriefcase"
              alt=""
              class="auth-stage__image block w-64 max-w-none md:w-80 lg:w-108"
            >
          </div>

          <div class="auth-panel">
            <div class="auth-panel__tabs">
              <button
                type="button"
                class="auth-panel__tab"
                :class="{ 'auth-panel__tab--active': isLogin }"
                @click="setMode('login')"
              >
                Вход
              </button>
              <button
                type="button"
                class="auth-panel__tab"
                :class="{ 'auth-panel__tab--active': !isLogin }"
                @click="setMode('register')"
              >
                Регистрация
              </button>
            </div>

            <form class="auth-form" @submit.prevent="isLogin ? handleLoginSubmit() : handleRegisterSubmit()">
              <div v-if="formError" class="auth-form__error">
                {{ formError }}
              </div>

              <div v-if="registrationInfo" class="auth-form__info">
                {{ registrationInfo }}
              </div>

              <label class="auth-form__field">
                <span class="auth-form__label">Логин</span>
                <input
                  v-model="currentLogin"
                  type="text"
                  placeholder="логин"
                  class="auth-form__input"
                  :class="inputClass('login')"
                  @input="clearFieldError('login')"
                />
                <span v-if="fieldErrors.login" class="auth-form__field-error">
                  {{ fieldErrors.login }}
                </span>
              </label>

              <div class="auth-form__grid" :class="{ 'auth-form__grid--single': isLogin }">
                <label class="auth-form__field">
                  <span class="auth-form__label">Пароль</span>
                  <input
                    v-model="currentPassword"
                    type="password"
                    placeholder="пароль"
                    class="auth-form__input"
                    :class="inputClass('password')"
                    @input="clearFieldError('password')"
                  />
                  <span v-if="fieldErrors.password" class="auth-form__field-error">
                    {{ fieldErrors.password }}
                  </span>
                </label>

                <label v-if="!isLogin" class="auth-form__field">
                  <span class="auth-form__label">Повтор пароля</span>
                  <input
                    v-model="registerForm.passwordRepeat"
                    type="password"
                    placeholder="еще раз пароль"
                    class="auth-form__input"
                    :class="inputClass('passwordRepeat')"
                    @input="clearFieldError('passwordRepeat')"
                  />
                  <span v-if="fieldErrors.passwordRepeat" class="auth-form__field-error">
                    {{ fieldErrors.passwordRepeat }}
                  </span>
                </label>
              </div>

              <template v-if="!isLogin">
                <div class="auth-form__grid auth-form__grid--compact">
                  <label class="auth-form__field">
                    <span class="auth-form__label">Возраст</span>
                    <input
                      v-model="registerForm.age"
                      type="number"
                      min="16"
                      max="100"
                      placeholder="например, 18"
                      class="auth-form__input"
                      :class="inputClass('age')"
                      @input="clearFieldError('age')"
                    />
                    <span v-if="fieldErrors.age" class="auth-form__field-error">
                      {{ fieldErrors.age }}
                    </span>
                  </label>

                  <label class="auth-form__field">
                    <span class="auth-form__label">Пол</span>
                    <select
                      v-model="registerForm.sex"
                      class="auth-form__input auth-form__select"
                      :class="inputClass('sex')"
                    >
                      <option value="male">Мужской</option>
                      <option value="female">Женский</option>
                    </select>
                  </label>
                </div>

                <div class="auth-form__grid auth-form__grid--compact">
                  <label class="auth-form__field">
                    <span class="auth-form__label">Образование</span>
                    <select
                      v-model="registerForm.educationLevel"
                      class="auth-form__input auth-form__select"
                      :class="inputClass('education_level')"
                    >
                      <option v-for="option in educationOptions" :key="option.value" :value="option.value">
                        {{ option.label }}
                      </option>
                    </select>
                  </label>

                  <label class="auth-form__field">
                    <span class="auth-form__label">Опыт, месяцев</span>
                    <input
                      v-model="registerForm.workExperienceMonths"
                      type="number"
                      min="0"
                      placeholder="например, 6"
                      class="auth-form__input"
                      :class="inputClass('work_experience_months')"
                      @input="clearFieldError('work_experience_months')"
                    />
                    <span v-if="fieldErrors.work_experience_months" class="auth-form__field-error">
                      {{ fieldErrors.work_experience_months }}
                    </span>
                  </label>
                </div>

                <label class="auth-form__field">
                  <span class="auth-form__label">Интересы и хобби</span>
                  <input
                  v-model="registerForm.hobbiesText"
                  type="text"
                  placeholder="ваши интересы"
                  class="auth-form__input"
                  :class="inputClass('hobbies_text')"
                  @input="clearFieldError('hobbies_text')"
                />
                  <span v-if="fieldErrors.hobbies_text" class="auth-form__field-error">
                    {{ fieldErrors.hobbies_text }}
                  </span>
                </label>
              </template>

              <button
                type="submit"
                class="auth-form__submit"
                :disabled="isSubmitting"
              >
                {{ isSubmitting ? 'Подождите...' : isLogin ? 'Войти' : 'Зарегистрироваться' }}
              </button>
            </form>
          </div>
        </div>
      </section>
    </main>

    <SiteFooter />
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import cameraImage from '@/assets/camera.png'
import CareerTestBlock from '@/components/CareerTestBlock.vue'
import SiteFooter from '@/components/SiteFooter.vue'
import SiteHeader from '@/components/ThemedSiteHeader.vue'
import authFloatingBriefcase from '@/assets/auth-floating-briefcase.png'
import authFloatingCoin from '@/assets/auth-floating-coin.png'
import backgroundObjectDark from '@/assets/background-green.png'
import paintKitImage from '@/assets/paint-kit.png'
import { loginUser, registerUser } from '@/lib/api'
import {
  STORAGE_KEYS,
  readStorageJson,
  readStorageValue,
  removeStorageValue,
  writeStorageJson,
  writeStorageValue,
} from '@/lib/storage'

const mode = ref('register')
const router = useRouter()
const route = useRoute()

const isLogin = computed(() => mode.value === 'login')
const isSubmitting = ref(false)
const formError = ref('')
const registrationInfo = ref('')
const fieldErrors = ref({})
const attemptToken = ref(readStorageValue(STORAGE_KEYS.attemptToken))
const previewResult = ref(readStorageJson(STORAGE_KEYS.testPreview))
const pendingRegistration = ref(readStorageJson(STORAGE_KEYS.pendingRegistration))

const loginForm = reactive({
  login: '',
  password: '',
})

const registerForm = reactive({
  login: '',
  password: '',
  passwordRepeat: '',
  age: '',
  sex: 'male',
  educationLevel: 'bachelor',
  workExperienceMonths: '',
  hobbiesText: '',
})

const educationOptions = [
  { value: 'school', label: 'Школа' },
  { value: 'college', label: 'Колледж' },
  { value: 'bachelor', label: 'Бакалавриат' },
  { value: 'master', label: 'Магистратура' },
  { value: 'specialist', label: 'Специалитет' },
]

const LOCKED_PREVIEW_TEXT = `РЕКОМЕНДАЦИИ СПЕЦИАЛЬНО ДЛЯ ВАС!
Ваш текущий фундамент позволяет совершить быстрый переход в разработку. Мы рекомендует сфокусироваться на Backend-направлении. В первую очередь стоит углубиться в изучение фреймворка Django или FastAPI, так как они наиболее востребованы на рынке. Параллельно с этим освойте работу с базами данных (PostgreSQL) и принципы построения API.

Как можно повысить квалификацию?
Реализуйте проект «Сервис доставки» с использованием асинхронности.
Изучите Docker для контейнеризации своих приложений.
Пройдите курс по архитектуре распределенных систем.`

const lockedPreviewParagraphs = LOCKED_PREVIEW_TEXT.split('\n').filter(Boolean)
const previewScores = computed(() => (
  Array.isArray(previewResult.value?.scores) ? previewResult.value.scores : []
))

const previewScoreTitles = computed(() => (
  previewScores.value
    .map((item) => item.title?.trim())
    .filter(Boolean)
))

const previewScoreLabels = computed(() => (
  previewScores.value
    .map((item) => item.label?.trim())
    .filter(Boolean)
))

const professionalTendencies = computed(() => (
  Array.isArray(previewResult.value?.professional_tendencies)
    ? previewResult.value.professional_tendencies.map((item) => String(item).trim()).filter(Boolean)
    : []
))

const authBackgroundObjectStyle = computed(() => ({
  backgroundImage: `url(${backgroundObjectDark})`,
}))

function joinHumanList(items) {
  if (!items.length) {
    return ''
  }

  if (items.length === 1) {
    return items[0]
  }

  if (items.length === 2) {
    return `${items[0]} и ${items[1]}`
  }

  return `${items.slice(0, -1).join(', ')} и ${items[items.length - 1]}`
}

const previewQualitiesText = computed(() => {
  const summary = previewResult.value?.preview_summary
    ?.replace(/^Тест пройден\.\s*/i, '')
    .trim()
  const titles = joinHumanList(previewScoreTitles.value)

  if (titles && summary) {
    return `${summary} По результатам теста у вас проявились такие направления: ${titles}.`
  }

  return summary || 'Мы уже подготовили краткое описание ваших сильных сторон по результатам теста.'
})

const previewCareerFitText = computed(() => {
  if (professionalTendencies.value.length) {
    return professionalTendencies.value.join(' ')
  }

  if (previewScoreLabels.value.length) {
    return previewScoreLabels.value.join(' ')
  }

  return previewResult.value?.preview_summary?.trim()
    || 'Мы уже определили ваши ведущие профессиональные склонности и готовы показать подробный разбор после регистрации.'
})

function scrollToAuthBlock() {
  const authBlock = document.getElementById('auth-panel')

  if (!authBlock) {
    return
  }

  authBlock.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
  })
}

async function syncAuthHashScroll() {
  if (route.hash !== '#auth-panel') {
    return
  }

  await nextTick()
  window.requestAnimationFrame(() => {
    scrollToAuthBlock()
  })
}

const currentLogin = computed({
  get: () => (isLogin.value ? loginForm.login : registerForm.login),
  set: (value) => {
    if (isLogin.value) {
      loginForm.login = value
      return
    }

    registerForm.login = value
  },
})

const currentPassword = computed({
  get: () => (isLogin.value ? loginForm.password : registerForm.password),
  set: (value) => {
    if (isLogin.value) {
      loginForm.password = value
      return
    }

    registerForm.password = value
  },
})

function setMode(nextMode) {
  mode.value = nextMode
  formError.value = ''
  registrationInfo.value = ''
  fieldErrors.value = {}
}

function setFieldError(field, message) {
  fieldErrors.value = {
    ...fieldErrors.value,
    [field]: message,
  }
}

function validateLoginForm() {
  fieldErrors.value = {}

  const login = loginForm.login.trim()
  const password = loginForm.password

  if (login.length < 3) {
    setFieldError('login', 'Логин должен содержать минимум 3 символа.')
  }

  if (login.length > 255) {
    setFieldError('login', 'Логин не должен превышать 255 символов.')
  }

  if (password.length < 8) {
    setFieldError('password', 'Пароль должен содержать минимум 8 символов.')
  }

  if (password.length > 128) {
    setFieldError('password', 'Пароль не должен превышать 128 символов.')
  }

  return Object.keys(fieldErrors.value).length === 0
}

function validateRegisterForm() {
  fieldErrors.value = {}

  const login = registerForm.login.trim()
  const password = registerForm.password
  const age = Number(registerForm.age)
  const workExperienceMonths = registerForm.workExperienceMonths === ''
    ? null
    : Number(registerForm.workExperienceMonths)
  const hobbiesText = registerForm.hobbiesText.trim()

  if (login.length < 3) {
    setFieldError('login', 'Логин должен содержать минимум 3 символа.')
  }

  if (login.length > 255) {
    setFieldError('login', 'Логин не должен превышать 255 символов.')
  }

  if (password.length < 8) {
    setFieldError('password', 'Пароль должен содержать минимум 8 символов.')
  }

  if (password.length > 128) {
    setFieldError('password', 'Пароль не должен превышать 128 символов.')
  }

  if (registerForm.passwordRepeat !== password) {
    setFieldError('passwordRepeat', 'Пароли должны совпадать.')
  }

  if (!Number.isInteger(age) || age < 16 || age > 100) {
    setFieldError('age', 'Возраст должен быть целым числом от 16 до 100.')
  }

  if (workExperienceMonths !== null && (!Number.isInteger(workExperienceMonths) || workExperienceMonths < 0)) {
    setFieldError('work_experience_months', 'Опыт должен быть целым числом месяцев от 0 и больше.')
  }

  if (hobbiesText.length > 2000) {
    setFieldError('hobbies_text', 'Поле с интересами не должно превышать 2000 символов.')
  }

  return !formError.value && Object.keys(fieldErrors.value).length === 0
}

function persistAuth(authResponse, options = {}) {
  writeStorageValue(STORAGE_KEYS.authFlag, 'true')
  writeStorageValue(STORAGE_KEYS.accessToken, authResponse.access_token)
  writeStorageJson(STORAGE_KEYS.authUser, authResponse.user)
  writeStorageValue(
    STORAGE_KEYS.authLoading,
    options.withLoading || authResponse.job_id ? 'true' : 'false',
  )

  if (authResponse.job_id) {
    writeStorageJson(STORAGE_KEYS.authJob, {
      jobId: authResponse.job_id,
      jobStatus: authResponse.job_status,
    })
    return
  }

  removeStorageValue(STORAGE_KEYS.authJob)
}

function buildRegisterPayload(attemptTokenValue) {
  return {
    login: registerForm.login.trim(),
    password: registerForm.password,
    attempt_token: attemptTokenValue,
    age: Number(registerForm.age),
    sex: registerForm.sex,
    education_level: registerForm.educationLevel,
    work_experience_months: registerForm.workExperienceMonths === '' ? null : Number(registerForm.workExperienceMonths),
    hobbies_text: registerForm.hobbiesText.trim() || null,
  }
}

function persistProfileDraft(payload) {
  writeStorageJson(STORAGE_KEYS.profileDraft, {
    age: payload.age,
    sex: payload.sex,
    educationLevel: payload.education_level,
    workExperienceMonths: payload.work_experience_months,
    hobbiesText: payload.hobbies_text,
  })
}

function syncRegisterFormWithPending(payload) {
  if (!payload) {
    return
  }

  registerForm.login = payload.login ?? registerForm.login
  registerForm.password = payload.password ?? registerForm.password
  registerForm.passwordRepeat = payload.password ?? registerForm.passwordRepeat
  registerForm.age = payload.age != null ? String(payload.age) : registerForm.age
  registerForm.sex = payload.sex ?? registerForm.sex
  registerForm.educationLevel = payload.education_level ?? registerForm.educationLevel
  registerForm.workExperienceMonths = payload.work_experience_months != null ? String(payload.work_experience_months) : ''
  registerForm.hobbiesText = payload.hobbies_text ?? registerForm.hobbiesText
}

async function finalizePendingRegistration() {
  if (isSubmitting.value || isLogin.value || !pendingRegistration.value || !attemptToken.value) {
    return
  }

  isSubmitting.value = true
  formError.value = ''
  registrationInfo.value = 'Завершаем регистрацию и запускаем детальный анализ.'

  const payload = {
    ...pendingRegistration.value,
    attempt_token: attemptToken.value,
  }

  try {
    const response = await registerUser(payload)

    persistProfileDraft(payload)
    pendingRegistration.value = null
    removeStorageValue(STORAGE_KEYS.pendingRegistration)
    removeStorageValue(STORAGE_KEYS.testResult)
    persistAuth(response, { withLoading: true })
    await router.push('/')
  } catch (error) {
    fieldErrors.value = error?.fieldErrors ?? {}
    formError.value = error?.message ?? 'Не удалось завершить регистрацию.'
    registrationInfo.value = ''
    mode.value = 'register'
    scrollToAuthBlock()
  } finally {
    isSubmitting.value = false
  }
}

async function handleLoginSubmit() {
  formError.value = ''

  if (!validateLoginForm()) {
    return
  }

  isSubmitting.value = true

  try {
    const response = await loginUser({
      login: loginForm.login.trim(),
      password: loginForm.password,
    })

    persistAuth(response)
    await router.push('/')
  } catch (error) {
    fieldErrors.value = error?.fieldErrors ?? {}
    formError.value = error?.message ?? 'Не удалось войти.'
  } finally {
    isSubmitting.value = false
  }
}

async function handleRegisterSubmit() {
  formError.value = ''
  registrationInfo.value = ''

  if (!validateRegisterForm()) {
    return
  }

  const attemptTokenValue = readStorageValue(STORAGE_KEYS.attemptToken)
  const payload = buildRegisterPayload(attemptTokenValue)

  if (!attemptTokenValue) {
    pendingRegistration.value = payload
    writeStorageJson(STORAGE_KEYS.pendingRegistration, payload)
    registrationInfo.value = 'Данные для регистрации сохранены. Чтобы получить анализ, пройдите тест выше.'
    await nextTick()
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
    return
  }

  isSubmitting.value = true

  try {
    const response = await registerUser(payload)

    persistProfileDraft(payload)
    pendingRegistration.value = null
    removeStorageValue(STORAGE_KEYS.pendingRegistration)
    removeStorageValue(STORAGE_KEYS.testResult)
    persistAuth(response, { withLoading: true })
    await router.push('/')
  } catch (error) {
    fieldErrors.value = error?.fieldErrors ?? {}
    formError.value = error?.message ?? 'Не удалось зарегистрироваться.'
  } finally {
    isSubmitting.value = false
  }
}

function inputClass(fieldName) {
  return fieldErrors.value[fieldName]
    ? 'auth-form__input--invalid'
    : ''
}

function clearFieldError(fieldName) {
  if (!fieldErrors.value[fieldName]) {
    return
  }

  const nextErrors = { ...fieldErrors.value }
  delete nextErrors[fieldName]
  fieldErrors.value = nextErrors
}

function handlePreviewUpdated(event) {
  previewResult.value = event.detail ?? readStorageJson(STORAGE_KEYS.testPreview)
  attemptToken.value = readStorageValue(STORAGE_KEYS.attemptToken)
  pendingRegistration.value = readStorageJson(STORAGE_KEYS.pendingRegistration)
  finalizePendingRegistration()
}

function handleStorageSync() {
  previewResult.value = readStorageJson(STORAGE_KEYS.testPreview)
  attemptToken.value = readStorageValue(STORAGE_KEYS.attemptToken)
  pendingRegistration.value = readStorageJson(STORAGE_KEYS.pendingRegistration)
  syncRegisterFormWithPending(pendingRegistration.value)
}

onMounted(() => {
  syncAuthHashScroll()
  syncRegisterFormWithPending(pendingRegistration.value)
  finalizePendingRegistration()

  window.addEventListener('career-ai:test-preview-updated', handlePreviewUpdated)
  window.addEventListener('storage', handleStorageSync)
  window.addEventListener('career-ai:storage-reset', handleStorageSync)
})

watch(
  () => route.hash,
  () => {
    syncAuthHashScroll()
  },
)

onBeforeUnmount(() => {
  window.removeEventListener('career-ai:test-preview-updated', handlePreviewUpdated)
  window.removeEventListener('storage', handleStorageSync)
  window.removeEventListener('career-ai:storage-reset', handleStorageSync)
})
</script>

<style scoped>
.auth-page {
  position: relative;
  background: linear-gradient(135deg, #161455 0%, #21176e 34%, #4a1d67 62%, #241782 100%);
  color: #fff;
}

.auth-page__background-object {
  position: absolute;
  left: 50%;
  top: 21rem;
  width: 100vw;
  height: 100vh;
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100% auto;
  pointer-events: none;
  transform: translate3d(-50%, -24%, 0);
  z-index: 0;
}

.auth-preview {
  position: relative;
}

.auth-preview__surface {
  position: relative;
  overflow: visible;
  padding: 0 0 4rem;
}

.auth-preview__intro {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
}

.auth-preview__title {
  margin: 0;
  max-width: 128rem;
  color: #ffd7eb;
  font-size: clamp(2.8rem, 6vw, 5.1rem);
  font-weight: 900;
  line-height: 1.02;
  text-transform: uppercase;
}

.auth-preview__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 3.5rem;
  margin-top: 4.5rem;
  align-items: stretch;
}

.auth-preview__feature {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) auto;
  align-items: center;
  justify-content: space-between;
  column-gap: 0.35rem;
  width: 100%;
}

.auth-preview__feature--right {
  grid-template-columns: auto minmax(0, 1.7fr);
}

.auth-preview__copy {
  position: relative;
  z-index: 1;
  max-width: 48rem;
  width: 100%;
}

.auth-preview__feature--right .auth-preview__copy {
  margin-left: auto;
  text-align: right;
}

.auth-preview__heading {
  margin: 0 0 0.9rem;
  color: #fff3fa;
  font-size: clamp(1.8rem, 2.8vw, 2.4rem);
  font-weight: 800;
  line-height: 1.05;
  text-transform: uppercase;
}

.auth-preview__text {
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.16rem;
  line-height: 1.32;
}

.auth-preview__art {
  position: relative;
  z-index: 0;
  align-self: center;
  flex-shrink: 0;
}

.auth-preview__art--camera {
  width: clamp(9.75rem, 12vw, 13rem);
}

.auth-preview__art--paint {
  width: clamp(10rem, 13vw, 13.5rem);
}

.auth-preview__art-image {
  display: block;
  width: 100%;
  height: auto;
  user-select: none;
  pointer-events: none;
  filter: drop-shadow(0 22px 44px rgba(27, 10, 87, 0.34));
}

.auth-preview__locked {
  position: relative;
  display: grid;
  place-items: center;
  z-index: 1;
  margin: 3.75rem auto 0;
  max-width: 44rem;
  min-height: 26rem;
  padding: 2rem 1.5rem 2.6rem;
}

.auth-preview__locked-text {
  grid-area: 1 / 1;
  width: 100%;
  position: relative;
  color: rgba(255, 255, 255, 0.72);
  opacity: 0.7;
  filter: blur(5px);
  user-select: none;
  pointer-events: none;
}

.auth-preview__locked-paragraph {
  margin: 0 0 1rem;
  font-size: 1.28rem;
  line-height: 1.42;
}

.auth-preview__locked-paragraph:last-child {
  margin-bottom: 0;
}

.auth-preview__overlay {
  grid-area: 1 / 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 1.4rem 1.25rem 0;
}

.auth-preview__overlay-kicker {
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.92rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.auth-preview__overlay-title {
  margin: 0.7rem 0 0;
  color: #fff;
  font-size: clamp(1.9rem, 3vw, 2.5rem);
  font-weight: 900;
  line-height: 1.02;
  text-transform: uppercase;
}

.auth-preview__overlay-text {
  margin: 1rem auto 0;
  max-width: 28rem;
  color: rgba(255, 255, 255, 0.86);
  font-size: 1.02rem;
  line-height: 1.35;
}

.auth-preview__overlay-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 11.5rem;
  min-height: 3.3rem;
  margin-top: 1.6rem;
  border-radius: 9999px;
  background: linear-gradient(180deg, #6f7fff 0%, #596eff 100%);
  padding: 0 1.9rem;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  box-shadow: 0 20px 40px rgba(77, 97, 255, 0.28);
  transition: transform 0.2s ease, opacity 0.2s ease, background-color 0.2s ease;
}

.auth-preview__overlay-button:hover {
  transform: translateY(-1px);
}

.auth-copy__title {
  margin: 0;
  color: #fff;
  font-size: clamp(3.1rem, 7vw, 5.1rem);
  font-weight: 900;
  line-height: 1.2;
  text-transform: uppercase;
  text-shadow: 0 12px 48px rgba(4, 2, 38, 0.26);
}

.auth-copy__subtitle {
  max-width: 25rem;
  margin-top: 2rem;
  color: #cac9ff;
  font-size: 0.95rem;
  line-height: 1.25;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.auth-stage {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 34rem;
  scroll-margin-top: 8rem;
}

.auth-stage__floating {
  z-index: 1;
}

.auth-stage__image {
  user-select: none;
  pointer-events: none;
  filter: drop-shadow(0 30px 80px rgba(23, 8, 72, 0.22));
}

.auth-stage__floating--coin {
  animation: floatCoin 6.8s ease-in-out infinite;
}

.auth-stage__floating--briefcase {
  animation: floatBriefcase 7.4s ease-in-out infinite;
}

.auth-panel {
  position: relative;
  z-index: 2;
  width: min(100%, 25.5rem);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 2rem;
  background: linear-gradient(180deg, rgba(237, 183, 255, 0.38), rgba(237, 183, 255, 0.2));
  box-shadow: 0 28px 80px rgba(9, 5, 40, 0.35);
  backdrop-filter: blur(28px);
  padding: 1.8rem 1.6rem 1.55rem;
}

.auth-panel__tabs {
  display: flex;
  gap: 1.2rem;
  margin-bottom: 1.5rem;
}

.auth-panel__tab {
  position: relative;
  padding-bottom: 0.45rem;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  transition: color 0.2s ease;
}

.auth-panel__tab--active {
  color: #fff;
}

.auth-panel__tab--active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 2px;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.84);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.auth-form__error {
  border: 1px solid rgba(255, 132, 156, 0.45);
  border-radius: 1rem;
  background: rgba(91, 13, 41, 0.22);
  padding: 0.85rem 1rem;
  color: #ffe6ef;
  font-size: 0.86rem;
  line-height: 1.4;
}

.auth-form__info {
  border: 1px solid rgba(124, 150, 255, 0.28);
  border-radius: 1rem;
  background: rgba(103, 121, 255, 0.12);
  padding: 0.85rem 1rem;
  color: #eef1ff;
  font-size: 0.86rem;
  line-height: 1.4;
}

.auth-form__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.85rem;
}

.auth-form__grid--single {
  grid-template-columns: 1fr;
}

.auth-form__grid--compact {
  gap: 0.75rem;
}

.auth-form__field {
  display: block;
}

.auth-form__label {
  display: block;
  margin-bottom: 0.35rem;
  color: rgb(255, 255, 255);
  font-size: 0.77rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.auth-form__input {
  width: 100%;
  height: 2.7rem;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 0.72rem;
  background: rgba(255, 255, 255, 0.72);
  padding: 0 0.95rem;
  color: #2e2354;
  font-size: 0.88rem;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
}

.auth-form__input::placeholder {
  color: rgba(58, 48, 99, 0.44);
}

.auth-form__input:focus {
  border-color: rgba(99, 120, 255, 0.82);
  box-shadow: 0 0 0 4px rgba(109, 124, 255, 0.16);
  background: rgba(255, 255, 255, 0.88);
}

.auth-form__input--invalid {
  border-color: rgba(255, 116, 151, 0.72);
  background: rgba(255, 230, 239, 0.86);
}

.auth-form__select {
  appearance: none;
}

.auth-form__field-error {
  display: block;
  margin-top: 0.35rem;
  color: #ffe1eb;
  font-size: 0.76rem;
  line-height: 1.35;
}

.auth-form__submit {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 2.9rem;
  border-radius: 0.82rem;
  background: linear-gradient(180deg, #587bff 0%, #5065ff 100%);
  color: #fff;
  font-size: 0.87rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.auth-form__submit:hover:not(:disabled) {
  transform: translateY(-1px);
}

.auth-form__submit:disabled {
  cursor: not-allowed;
  opacity: 0.72;
}

.auth-form__hint {
  align-self: center;
  color: rgba(255, 255, 255, 0.76);
  font-size: 0.72rem;
  font-weight: 600;
}

@keyframes floatCoin {
  0%, 100% {
    transform: translate3d(0, 0, 0) rotate(0deg);
  }
  50% {
    transform: translate3d(-18px, -8px, 0) rotate(-9deg);
  }
}

@keyframes floatBriefcase {
  0%, 100% {
    transform: translate3d(0, 0, 0) rotate(0deg);
  }
  50% {
    transform: translate3d(20px, -10px, 0) rotate(9deg);
  }
}

@media (max-width: 1023px) {
  .auth-page__background-object {
    width: 100vw;
    height: 46rem;
    background-size: 118% auto;
  }

  .auth-preview__surface {
    padding: 0 0 3rem;
  }

  .auth-preview__content {
    gap: 2.5rem;
    margin-top: 3rem;
  }

  .auth-preview__feature,
  .auth-preview__feature--right {
    grid-template-columns: minmax(0, 1.35fr) auto;
    column-gap: 0.5rem;
  }

  .auth-preview__feature--right .auth-preview__copy {
    margin-left: auto;
    text-align: right;
  }

  .auth-preview__text {
    max-width: 34rem;
    font-size: 1.05rem;
  }

  .auth-preview__art--camera {
    width: clamp(8rem, 16vw, 10rem);
  }

  .auth-preview__art--paint {
    width: clamp(8.25rem, 17vw, 10.5rem);
  }

  .auth-preview__locked {
    margin-top: 3.4rem;
  }

  .auth-preview__locked-paragraph {
    font-size: 1.08rem;
  }

  .auth-copy {
    text-align: center;
    margin: 0 auto;
  }

  .auth-copy__subtitle {
    margin-left: auto;
    margin-right: auto;
  }

  .auth-stage {
    min-height: 30rem;
  }
}

@media (max-width: 767px) {
  .auth-page__background-object {
    top: 17rem;
    width: 100vw;
    height: 34rem;
    background-size: 148% auto;
    transform: translate3d(-50%, -16%, 0);
  }

  .auth-preview {
    margin-top: 2.75rem;
  }

  .auth-preview__surface {
    padding: 2.4rem 0 2.2rem;
  }

  .auth-preview__title {
    font-size: 2.25rem;
  }

  .auth-preview__content {
    gap: 2rem;
    margin-top: 2.4rem;
  }

  .auth-preview__heading {
    font-size: 1.2rem;
  }

  .auth-preview__feature,
  .auth-preview__feature--right {
    grid-template-columns: minmax(0, 1.15fr) auto;
    column-gap: 0.45rem;
  }

  .auth-preview__feature--left {
    grid-template-columns: minmax(0, 1fr) clamp(5.5rem, 18vw, 7rem);
  }

  .auth-preview__feature--right {
    grid-template-columns: clamp(5.75rem, 19vw, 7.25rem) minmax(0, 1fr);
  }

  .auth-preview__copy {
    max-width: none;
  }

  .auth-preview__feature--right .auth-preview__copy {
    padding-left: 0.35rem;
    text-align: right;
  }

  .auth-preview__text {
    font-size: 0.9rem;
    line-height: 1.34;
  }

  .auth-preview__art--camera {
    width: clamp(5.5rem, 18vw, 7rem);
  }

  .auth-preview__art--paint {
    width: clamp(5.75rem, 19vw, 7.25rem);
  }

  .auth-preview__locked {
    max-width: 100%;
    margin-top: 2.4rem;
    min-height: 22rem;
    padding: 1rem 0 1.4rem;
  }

  .auth-preview__locked-text {
    opacity: 0.76;
    filter: blur(4px);
  }

  .auth-preview__locked-paragraph {
    font-size: 0.94rem;
    line-height: 1.5;
  }

  .auth-preview__overlay {
    position: relative;
    padding: 0 0.35rem;
  }

  .auth-preview__overlay-kicker {
    font-size: 0.72rem;
  }

  .auth-preview__overlay-title {
    font-size: 1.5rem;
  }

  .auth-preview__overlay-text {
    font-size: 0.88rem;
  }

  .auth-preview__overlay-button {
    min-width: 10rem;
    min-height: 2.9rem;
    margin-top: 1.2rem;
    font-size: 0.76rem;
  }

  .auth-copy__title {
    font-size: 2rem;
  }

  .auth-copy__subtitle {
    margin-top: 1rem;
    font-size: 0.8rem;
  }

  .auth-stage {
    min-height: 24rem;
  }

  .auth-stage__floating {
    opacity: 0.92;
  }

  .auth-panel {
    width: 100%;
    padding: 1.25rem 1rem 1.1rem;
  }

  .auth-panel__tabs {
    gap: 0.8rem;
    margin-bottom: 1rem;
  }

  .auth-panel__tab {
    font-size: 0.76rem;
  }

  .auth-form__grid,
  .auth-form__grid--compact {
    grid-template-columns: 1fr;
  }
}
</style>
