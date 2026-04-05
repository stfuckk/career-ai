import { createRouter, createWebHistory } from 'vue-router'

import { hasPersistedAuth, validatePersistedSession } from '@/lib/session'
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

router.beforeEach(async (to) => {
  if (!hasPersistedAuth()) {
    if (to.name !== 'auth') {
      return { name: 'auth' }
    }

    return true
  }

  const isSessionValid = await validatePersistedSession()

  if (!isSessionValid) {
    return { name: 'auth' }
  }

  if (to.name === 'auth') {
    return { name: 'home' }
  }

  return true
})

export default router
