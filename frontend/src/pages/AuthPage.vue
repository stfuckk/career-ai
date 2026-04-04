<template>
  <div class="auth-page flex min-h-screen flex-col overflow-hidden">
    <SiteHeader />

    <main class="relative z-10 flex flex-1 flex-col px-4 pb-8 pt-28 sm:px-8 sm:pt-32 lg:px-12 lg:pb-12 lg:pt-36">
      <div class="relative left-1/2 w-screen max-w-none -translate-x-1/2 overflow-hidden">
        <CareerTestBlock />
      </div>

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

        <div class="auth-stage">

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

              <label class="auth-form__field">
                <span class="auth-form__label">Логин</span>
                <input
                  v-model="currentLogin"
                  type="text"
                  placeholder="email"
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
                      max="22"
                      placeholder="16-22"
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
                      :class="inputClass('workExperienceMonths')"
                      @input="clearFieldError('workExperienceMonths')"
                    />
                    <span v-if="fieldErrors.workExperienceMonths" class="auth-form__field-error">
                      {{ fieldErrors.workExperienceMonths }}
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
                    :class="inputClass('hobbiesText')"
                    @input="clearFieldError('hobbiesText')"
                  />
                  <span v-if="fieldErrors.hobbiesText" class="auth-form__field-error">
                    {{ fieldErrors.hobbiesText }}
                  </span>
                </label>
              </template>

              <button
                type="submit"
                class="auth-form__submit"
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
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import CareerTestBlock from '@/components/CareerTestBlock.vue'
import SiteFooter from '@/components/SiteFooter.vue'
import SiteHeader from '@/components/ThemedSiteHeader.vue'
import authFloatingBriefcase from '@/assets/auth-floating-briefcase.png'
import authFloatingCoin from '@/assets/auth-floating-coin.png'
import { loginUser, registerUser } from '@/lib/api'
import {
  STORAGE_KEYS,
  readStorageValue,
  removeStorageValue,
  writeStorageJson,
  writeStorageValue,
} from '@/lib/storage'

const mode = ref('register')
const router = useRouter()

const isLogin = computed(() => mode.value === 'login')
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

function setMode(nextMode) {
  mode.value = nextMode
  formError.value = ''
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
  const attemptTokenValue = readStorageValue(STORAGE_KEYS.attemptToken)

  if (!attemptTokenValue) {
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

  const attemptTokenValue = readStorageValue(STORAGE_KEYS.attemptToken)
  const payload = {
    login: registerForm.login.trim(),
    password: registerForm.password,
    attempt_token: attemptTokenValue,
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
</script>

<style scoped>
.auth-page {
  position: relative;
  background: linear-gradient(135deg, #161455 0%, #21176e 34%, #4a1d67 62%, #241782 100%);
  color: #fff;
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
