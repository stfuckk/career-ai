<template>
  <header class="fixed inset-x-0 top-0 z-50 shrink-0 px-4 pt-4 sm:px-8 sm:pt-6 lg:px-12">
    <div class="authlike-header mx-auto flex w-full max-w-6xl items-center justify-between gap-4">
      <button
        type="button"
        class="authlike-header__icon-button"
        aria-label="Посмотреть вакансии"
        @click="goToVacancies"
      >
        <span class="authlike-header__icon authlike-header__icon--button">
          <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="6" />
            <path d="m20 20-3.5-3.5" />
          </svg>
        </span>
        <span class="authlike-header__tooltip">Посмотреть вакансии</span>
      </button>

      <RouterLink to="/" class="authlike-header__brand">
        ПрофАпдейт
      </RouterLink>

      <div class="authlike-header__actions">
        <button
          type="button"
          class="authlike-header__icon-button"
          aria-label="Авторизация"
          @click="goToAuthBlock"
        >
          <span class="authlike-header__icon authlike-header__icon--button">
            <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21a8 8 0 0 0-16 0" />
              <circle cx="12" cy="8" r="4" />
            </svg>
          </span>
          <span class="authlike-header__tooltip">Авторизация</span>
        </button>

        <button
          v-if="isAuthenticated"
          type="button"
          class="authlike-header__icon-button"
          aria-label="Выйти из аккаунта"
          @click="handleLogout"
        >
          <span class="authlike-header__icon authlike-header__icon--button">
            <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M10 17H6a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h4" />
              <path d="M15 7l5 5-5 5" />
              <path d="M20 12H9" />
            </svg>
          </span>
          <span class="authlike-header__tooltip">Выйти из аккаунта</span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { clearInvalidSession, hasPersistedAuth, validatePersistedSession } from '@/lib/session'

const router = useRouter()
const route = useRoute()
const authTick = ref(0)

const isAuthenticated = computed(() => {
  authTick.value
  return hasPersistedAuth()
})

function syncAuthState() {
  authTick.value += 1
}

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

async function goToAuthBlock() {
  if (hasPersistedAuth()) {
    const isSessionValid = await ensureSessionOrRedirect()

    if (!isSessionValid) {
      return
    }
  }

  if (route.name === 'auth') {
    scrollToAuthBlock()
    return
  }

  await router.push({ name: 'auth', hash: '#auth-panel' })
}

async function ensureSessionOrRedirect() {
  if (!hasPersistedAuth()) {
    await router.push({ name: 'auth' })
    return false
  }

  const isSessionValid = await validatePersistedSession()

  if (!isSessionValid) {
    syncAuthState()
    await router.push({ name: 'auth' })
    return false
  }

  syncAuthState()
  return true
}

async function goToVacancies() {
  const isSessionValid = await ensureSessionOrRedirect()

  if (!isSessionValid) {
    return
  }

  await router.push({ name: 'vacancies' })
}

async function handleLogout() {
  clearInvalidSession()
  syncAuthState()
  await router.push({ name: 'auth' })
}

onMounted(() => {
  window.addEventListener('storage', syncAuthState)
  window.addEventListener('career-ai:storage-reset', syncAuthState)
})

onBeforeUnmount(() => {
  window.removeEventListener('storage', syncAuthState)
  window.removeEventListener('career-ai:storage-reset', syncAuthState)
})
</script>

<style scoped>
.authlike-header {
  min-height: 3rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 9999px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.08));
  box-shadow: 0 22px 60px rgba(8, 5, 45, 0.18);
  backdrop-filter: blur(18px);
  color: rgba(255, 255, 255, 0.92);
  padding: 0.4rem 1rem;
}

.authlike-header__actions {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.authlike-header__icon-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.authlike-header__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 9999px;
  color: rgba(255, 255, 255, 0.86);
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.authlike-header__icon--button:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-1px);
}

.authlike-header__tooltip {
  position: absolute;
  top: calc(100% + 0.45rem);
  right: 50%;
  min-width: max-content;
  border-radius: 9999px;
  background: rgba(16, 11, 49, 0.92);
  padding: 0.36rem 0.72rem;
  color: rgba(255, 255, 255, 0.92);
  font-size: 0.76rem;
  line-height: 1.15;
  opacity: 0;
  pointer-events: none;
  transform: translateX(50%) translateY(-3px);
  transition: opacity 0.2s ease, transform 0.2s ease;
  white-space: nowrap;
}

.authlike-header__icon-button:hover .authlike-header__tooltip,
.authlike-header__icon-button:focus-visible .authlike-header__tooltip {
  opacity: 1;
  transform: translateX(50%) translateY(0);
}

.authlike-header__brand {
  font-size: 0.95rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  color: rgba(255, 255, 255, 0.92);
}

@media (max-width: 767px) {
  .authlike-header {
    padding-left: 0.7rem;
    padding-right: 0.7rem;
  }

  .authlike-header__brand {
    font-size: 0.88rem;
  }

  .authlike-header__actions {
    gap: 0.1rem;
  }
}
</style>
