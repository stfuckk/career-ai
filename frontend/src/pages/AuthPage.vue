<template>
  <div class="flex min-h-screen flex-col bg-(--page-bg-alt) transition-colors duration-300">
    <SiteHeader />

    <main class="flex flex-1">
      <section
        ref="heroSectionRef"
        class="auth-hero relative flex flex-1 items-center overflow-hidden px-0 py-10 sm:px-5 sm:py-14 lg:px-32 lg:py-10"
        @pointermove="handlePointerMove"
        @pointerleave="resetPointerOffset"
      >
        <div
          class="auth-hero__background"
          :class="{ 'auth-hero__background--dark': isDark }"
          :style="backgroundStyle"
          aria-hidden="true"
        />

        <div class="relative z-10 mx-auto grid w-full max-w-3xl gap-8 px-4 sm:max-w-155 sm:px-6 md:max-w-170 md:px-6 lg:max-w-7xl lg:grid-cols-[1.1fr_0.9fr] lg:items-center lg:gap-12 lg:px-10">
          <div class="max-w-xl text-(--text-hero) sm:max-w-155 md:max-w-170">
            <p class="text-sm font-semibold uppercase tracking-[0.24em] text-(--text-accent-soft)">
              Начнем
            </p>
            <h1 class="mt-4 text-4xl font-black uppercase leading-[0.95] tracking-[-0.04em] sm:text-6xl">
              {{ isLogin ? 'Вход в личный кабинет' : 'Создание аккаунта' }}
            </h1>
            <p class="mt-5 text-base leading-7 text-(--text-accent-soft) sm:text-lg">
              {{ isLogin
                ? 'Войдите, чтобы получить план развития и рекомендации по вакансиям.'
                : 'Зарегистрируйтесь бесплатно. Данные о вашем возрасте, поле, образовании и опыте используются только для подбора точных рекомендаций' }}
            </p>
          </div>

          <div class="rounded-4xl bg-(--surface) px-5 py-5 shadow-(--shadow-card) transition-colors duration-300 sm:mx-auto sm:w-full sm:max-w-155 sm:px-7 sm:py-6 md:max-w-170 lg:max-w-none">
            <div class="mb-5 flex gap-6 border-b border-(--border-soft) pb-3 text-lg font-bold uppercase">
              <button
                type="button"
                class="relative pb-1 transition"
                :class="isLogin ? 'text-(--text-main)' : 'text-(--text-muted)'"
                @click="setMode('login')"
              >
                Вход
                <span
                  v-if="isLogin"
                  class="absolute inset-x-0 -bottom-4.25 h-1 rounded-full bg-(--button-secondary)"
                />
              </button>
              <button
                type="button"
                class="relative pb-1 transition"
                :class="!isLogin ? 'text-(--text-main)' : 'text-(--text-muted)'"
                @click="setMode('register')"
              >
                Регистрация
                <span
                  v-if="!isLogin"
                  class="absolute inset-x-0 -bottom-4.25 h-1 rounded-full bg-(--button-secondary)"
                />
              </button>
            </div>

            <form class="space-y-3" @submit.prevent="isLogin ? handleLoginSubmit() : handleRegisterSubmit()">
              <div
                v-if="formError"
                class="rounded-2xl border border-rose-400/35 bg-rose-500/8 px-4 py-3 text-sm text-rose-700 dark:text-rose-200"
              >
                {{ formError }}
              </div>

              <label class="block">
                <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Логин</span>
                <input
                  v-model="currentLogin"
                  type="text"
                  placeholder="Логин"
                  class="h-11 w-full rounded-xl border px-4 text-sm text-(--text-main) outline-none transition placeholder:text-(--text-muted) focus:border-(--button-secondary)"
                  :class="inputClass('login')"
                  @input="clearFieldError('login')"
                />
                <span v-if="fieldErrors.login" class="mt-2 block text-sm text-rose-600 dark:text-rose-300">
                  {{ fieldErrors.login }}
                </span>
              </label>

              <div :class="isLogin ? 'block' : 'grid gap-3 sm:grid-cols-2'">
                <label class="block">
                  <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Пароль</span>
                  <input
                    v-model="currentPassword"
                    type="password"
                    placeholder="Введите пароль"
                    class="h-11 w-full rounded-xl border px-4 text-sm text-(--text-main) outline-none transition placeholder:text-(--text-muted) focus:border-(--button-secondary)"
                    :class="inputClass('password')"
                    @input="clearFieldError('password')"
                  />
                  <span v-if="fieldErrors.password" class="mt-2 block text-sm text-rose-600 dark:text-rose-300">
                    {{ fieldErrors.password }}
                  </span>
                </label>

                <label v-if="!isLogin" class="block">
                  <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Повторите пароль</span>
                  <input
                    v-model="registerForm.passwordRepeat"
                    type="password"
                    placeholder="Повторите пароль"
                    class="h-11 w-full rounded-xl border px-4 text-sm text-(--text-main) outline-none transition placeholder:text-(--text-muted) focus:border-(--button-secondary)"
                    :class="inputClass('passwordRepeat')"
                    @input="clearFieldError('passwordRepeat')"
                  />
                  <span
                    v-if="fieldErrors.passwordRepeat"
                    class="mt-2 block text-sm text-rose-600 dark:text-rose-300"
                  >
                    {{ fieldErrors.passwordRepeat }}
                  </span>
                </label>
              </div>

              <template v-if="!isLogin">
                
                <div class="grid gap-3 sm:grid-cols-2">
                  <label class="block">
                    <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Возраст</span>
                    <input
                      v-model="registerForm.age"
                      type="number"
                      min="16"
                      max="22"
                      placeholder="16-22"
                      class="h-11 w-full rounded-xl border px-4 text-sm text-(--text-main) outline-none transition placeholder:text-(--text-muted) focus:border-(--button-secondary)"
                      :class="inputClass('age')"
                      @input="clearFieldError('age')"
                    />
                    <span v-if="fieldErrors.age" class="mt-2 block text-sm text-rose-600 dark:text-rose-300">
                      {{ fieldErrors.age }}
                    </span>
                  </label>

                  <label class="block">
                    <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Пол</span>
                    <select
                      v-model="registerForm.sex"
                      class="h-11 w-full rounded-xl border px-4 text-sm text-(--text-main) outline-none transition focus:border-(--button-secondary)"
                      :class="inputClass('sex')"
                    >
                      <option value="male">Мужской</option>
                      <option value="female">Женский</option>
                    </select>
                  </label>
                </div>

                <div class="grid gap-3 sm:grid-cols-2">
                  <label class="block">
                    <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Образование</span>
                    <select
                      v-model="registerForm.educationLevel"
                      class="h-11 w-full rounded-xl border px-4 text-sm text-(--text-main) outline-none transition focus:border-(--button-secondary)"
                      :class="inputClass('education_level')"
                    >
                      <option v-for="option in educationOptions" :key="option.value" :value="option.value">
                        {{ option.label }}
                      </option>
                    </select>
                  </label>

                  <label class="block">
                    <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Опыт работы, месяцев</span>
                    <input
                      v-model="registerForm.workExperienceMonths"
                      type="number"
                      min="0"
                      placeholder="Например, 6"
                      class="h-11 w-full rounded-xl border px-4 text-sm text-(--text-main) outline-none transition placeholder:text-(--text-muted) focus:border-(--button-secondary)"
                      :class="inputClass('workExperienceMonths')"
                      @input="clearFieldError('workExperienceMonths')"
                    />
                    <span
                      v-if="fieldErrors.workExperienceMonths"
                      class="mt-2 block text-sm text-rose-600 dark:text-rose-300"
                    >
                      {{ fieldErrors.workExperienceMonths }}
                    </span>
                  </label>
                </div>

                <label class="block">
                  <span class="mb-2 block text-sm font-medium text-(--text-main)/70">Интересы и хобби</span>
                  <input
                    v-model="registerForm.hobbiesText"
                    type="text"
                    placeholder="Например, люблю анализировать данные, читать о технологиях."
                    class="h-11 w-full rounded-xl border px-4 text-sm text-(--text-main) outline-none transition placeholder:text-(--text-muted) focus:border-(--button-secondary)"
                    :class="inputClass('hobbiesText')"
                    @input="clearFieldError('hobbiesText')"
                  />
                  <span v-if="fieldErrors.hobbiesText" class="mt-2 block text-sm text-rose-600 dark:text-rose-300">
                    {{ fieldErrors.hobbiesText }}
                  </span>
                </label>
              </template>

              <button
                type="submit"
                class="mt-1 flex h-11 w-full items-center justify-center rounded-xl bg-(--button-secondary) text-sm font-bold uppercase tracking-[0.08em] text-(--button-text) shadow-[0_12px_26px_rgba(90,102,255,0.28)] transition hover:bg-(--button-secondary-hover) disabled:cursor-not-allowed disabled:opacity-70"
                :disabled="isSubmitting || (!isLogin && !attemptToken)"
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
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import backgroundObjectDark from '@/assets/background-object-dark.png'
import backgroundObjectLight from '@/assets/background-object-light.png'
import SiteFooter from '@/components/SiteFooter.vue'
import SiteHeader from '@/components/ThemedSiteHeader.vue'
import { useTheme } from '@/composables/useTheme'
import { loginUser, registerUser } from '@/lib/api'
import {
  STORAGE_KEYS,
  readStorageValue,
  removeStorageValue,
  writeStorageJson,
  writeStorageValue,
} from '@/lib/storage'

const mode = ref('register')
const { isDark } = useTheme()
const router = useRouter()

const isLogin = computed(() => mode.value === 'login')
const heroSectionRef = ref(null)
const isInteractive = ref(false)
const pointerOffset = ref({ x: 0, y: 0 })
const isSubmitting = ref(false)
const formError = ref('')
const fieldErrors = ref({})
const attemptToken = computed(() => readStorageValue(STORAGE_KEYS.attemptToken))

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

let animationFrameId = 0
let mediaQueryList = null
let currentOffsetX = 0
let currentOffsetY = 0
let targetOffsetX = 0
let targetOffsetY = 0

const backgroundStyle = computed(() => ({
  '--auth-bg-image': `url(${isDark.value ? backgroundObjectDark : backgroundObjectLight})`,
  '--auth-bg-offset-x': `${pointerOffset.value.x}px`,
  '--auth-bg-offset-y': `${pointerOffset.value.y}px`,
}))

function setMode(nextMode) {
  mode.value = nextMode
  formError.value = ''
  fieldErrors.value = {}
}

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
  const attemptToken = readStorageValue(STORAGE_KEYS.attemptToken)

  if (!attemptToken) {
    formError.value = 'Сначала пройдите тест, чтобы мы могли связать регистрацию с результатом.'
  }

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

  if (!Number.isInteger(age) || age < 16 || age > 22) {
    setFieldError('age', 'Возраст должен быть целым числом от 16 до 22.')
  }

  if (workExperienceMonths !== null && (!Number.isInteger(workExperienceMonths) || workExperienceMonths < 0)) {
    setFieldError('workExperienceMonths', 'Опыт должен быть целым числом месяцев от 0 и больше.')
  }

  if (hobbiesText.length > 2000) {
    setFieldError('hobbiesText', 'Поле с интересами не должно превышать 2000 символов.')
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

  if (!validateRegisterForm()) {
    return
  }

  const attemptToken = readStorageValue(STORAGE_KEYS.attemptToken)
  const payload = {
    login: registerForm.login.trim(),
    password: registerForm.password,
    attempt_token: attemptToken,
    age: Number(registerForm.age),
    sex: registerForm.sex,
    education_level: registerForm.educationLevel,
    work_experience_months: registerForm.workExperienceMonths === '' ? null : Number(registerForm.workExperienceMonths),
    hobbies_text: registerForm.hobbiesText.trim() || null,
  }

  isSubmitting.value = true

  try {
    const response = await registerUser(payload)

    writeStorageJson(STORAGE_KEYS.profileDraft, {
      age: payload.age,
      sex: payload.sex,
      educationLevel: payload.education_level,
      workExperienceMonths: payload.work_experience_months,
      hobbiesText: payload.hobbies_text,
    })
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
    ? 'border-rose-400 bg-rose-500/6'
    : 'border-transparent bg-(--surface-soft)'
}

function clearFieldError(fieldName) {
  if (!fieldErrors.value[fieldName]) {
    return
  }

  const nextErrors = { ...fieldErrors.value }
  delete nextErrors[fieldName]
  fieldErrors.value = nextErrors
}

onMounted(() => {
  mediaQueryList = window.matchMedia('(min-width: 768px) and (pointer: fine)')
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
.auth-hero {
  isolation: isolate;
}

.auth-hero__background {
  position: absolute;
  top: 21rem;
  left: 50%;
  width: min(88vw, 1120px);
  aspect-ratio: 1 / 1;
  background-image: var(--auth-bg-image);
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  opacity: 0.92;
  pointer-events: none;
  transform: translate3d(
    calc(-50% + var(--auth-bg-offset-x, 0px)),
    calc(-50% + var(--auth-bg-offset-y, 0px)),
    0
  );
  transition: opacity 0.3s ease;
  z-index: 0;
}

.auth-hero__background--dark {
  opacity: 0.88;
}

@media (max-width: 767px), (pointer: coarse) {
  .auth-hero__background {
    top: 18rem;
    width: min(135vw, 820px);
    opacity: 0.82;
    transform: translate3d(-50%, -44%, 0);
  }
}
</style>
