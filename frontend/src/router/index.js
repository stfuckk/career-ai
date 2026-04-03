import { createRouter, createWebHistory } from 'vue-router'

import AuthPage from '@/pages/AuthPage.vue'
import HomePage from '@/pages/HomePage.vue'

const router = createRouter({
  history: createWebHistory(),
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
  ],
})

export default router
