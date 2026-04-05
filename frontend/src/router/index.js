import { createRouter, createWebHistory } from 'vue-router'

import { readCurrentUser } from '@/lib/api'
import { STORAGE_KEYS, clearAuthStorage, readStorageValue, writeStorageJson } from '@/lib/storage'
import AuthPage from '@/pages/AuthPage.vue'
import HomePage from '@/pages/HomePage.vue'
import VacanciesPage from '@/pages/VacanciesPage.vue'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior() {
    return { top: 0 }
  },
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/auth',
      name: 'auth',
      component: AuthPage,
    },
    {
      path: '/test',
      name: 'career-test',
      redirect: '/auth',
    },
    {
      path: '/vacancies',
      name: 'vacancies',
      component: VacanciesPage,
    },
  ],
})

let authValidationPromise = null

function hasPersistedAuth() {
  return readStorageValue(STORAGE_KEYS.authFlag) === 'true' || Boolean(readStorageValue(STORAGE_KEYS.accessToken))
}

function clearInvalidSession() {
  clearAuthStorage()
}

async function validatePersistedSession() {
  const token = readStorageValue(STORAGE_KEYS.accessToken)

  if (!token) {
    clearInvalidSession()
    return false
  }

  if (!authValidationPromise) {
    authValidationPromise = readCurrentUser(token)
      .then((user) => {
        writeStorageJson(STORAGE_KEYS.authUser, user)
        return true
      })
      .catch((error) => {
        if (error?.status === 401 || error?.status === 403) {
          clearInvalidSession()
          return false
        }

        return true
      })
      .finally(() => {
        authValidationPromise = null
      })
  }

  return authValidationPromise
}

router.beforeEach(async (to) => {
  if (!hasPersistedAuth()) {
    if (to.name === 'home') {
      return { name: 'auth' }
    }

    return true
  }

  const isSessionValid = await validatePersistedSession()

  if (!isSessionValid) {
    return { name: 'auth' }
  }

  return true
})

export default router
