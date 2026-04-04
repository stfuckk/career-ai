import { createRouter, createWebHistory } from 'vue-router'

import AuthPage from '@/pages/AuthPage.vue'
import CareerTestPage from '@/pages/CareerTestPage.vue'
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
      component: CareerTestPage,
    },
    {
      path: '/vacancies',
      name: 'vacancies',
      component: VacanciesPage,
    },
  ],
})

export default router
