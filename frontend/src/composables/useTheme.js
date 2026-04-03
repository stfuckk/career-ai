import { computed, ref } from 'vue'

const STORAGE_KEY = 'career-ai-theme'
const theme = ref('light')

function applyTheme(nextTheme) {
  if (typeof document === 'undefined') {
    return
  }

  document.documentElement.classList.toggle('theme-dark', nextTheme === 'dark')
}

function setTheme(nextTheme) {
  theme.value = nextTheme
  applyTheme(nextTheme)

  if (typeof window !== 'undefined') {
    window.localStorage.setItem(STORAGE_KEY, nextTheme)
  }
}

function initTheme() {
  if (typeof window === 'undefined') {
    return
  }

  const savedTheme = window.localStorage.getItem(STORAGE_KEY)
  setTheme(savedTheme === 'dark' ? 'dark' : 'light')
}

export function useTheme() {
  const isDark = computed(() => theme.value === 'dark')

  function toggleTheme() {
    setTheme(isDark.value ? 'light' : 'dark')
  }

  return {
    theme,
    isDark,
    toggleTheme,
    initTheme,
  }
}
