<template>
  <header class="fixed inset-x-0 top-0 z-50 shrink-0 px-4 pt-4 sm:px-8 sm:pt-6 lg:px-12">
    <div class="authlike-header mx-auto flex w-full max-w-6xl items-center justify-between gap-4">
      <RouterLink to="/vacancies" class="authlike-header__icon" aria-label="Вакансии">
        <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="6" />
          <path d="m20 20-3.5-3.5" />
        </svg>
      </RouterLink>

      <RouterLink to="/" class="authlike-header__brand">
        ПрофАпдейт
      </RouterLink>

      <button
        type="button"
        class="authlike-header__icon"
        aria-label="Профиль"
        @click="goToAuthBlock"
      >
        <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21a8 8 0 0 0-16 0" />
          <circle cx="12" cy="8" r="4" />
        </svg>
      </button>
    </div>
  </header>
</template>

<script setup>
import { RouterLink, useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

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
  if (route.name === 'auth') {
    scrollToAuthBlock()
    return
  }

  await router.push({ name: 'auth', hash: '#auth-panel' })
}
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

.authlike-header__icon:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-1px);
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
}
</style>
