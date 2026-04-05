export const STORAGE_KEYS = {
  authFlag: 'career-ai-demo-auth',
  accessToken: 'career-ai-access-token',
  authUser: 'career-ai-auth-user',
  profileDraft: 'career-ai-profile-draft',
  testScores: 'career-ai-test-results',
  testPreview: 'career-ai-test-preview',
  testResult: 'career-ai-test-result',
  attemptToken: 'career-ai-attempt-token',
  authLoading: 'career-ai-auth-loading',
  authJob: 'career-ai-auth-job',
  pendingRegistration: 'career-ai-pending-registration',
}

function isBrowser() {
  return typeof window !== 'undefined'
}

export function readStorageValue(key) {
  if (!isBrowser()) {
    return null
  }

  return window.localStorage.getItem(key)
}

export function writeStorageValue(key, value) {
  if (!isBrowser()) {
    return
  }

  window.localStorage.setItem(key, value)
}

export function removeStorageValue(key) {
  if (!isBrowser()) {
    return
  }

  window.localStorage.removeItem(key)
}

export function readStorageJson(key, fallback = null) {
  const value = readStorageValue(key)

  if (!value) {
    return fallback
  }

  try {
    return JSON.parse(value)
  } catch {
    return fallback
  }
}

export function writeStorageJson(key, value) {
  writeStorageValue(key, JSON.stringify(value))
}

export function clearAuthStorage() {
  removeStorageValue(STORAGE_KEYS.authFlag)
  removeStorageValue(STORAGE_KEYS.accessToken)
  removeStorageValue(STORAGE_KEYS.authUser)
  removeStorageValue(STORAGE_KEYS.profileDraft)
  removeStorageValue(STORAGE_KEYS.testScores)
  removeStorageValue(STORAGE_KEYS.testPreview)
  removeStorageValue(STORAGE_KEYS.testResult)
  removeStorageValue(STORAGE_KEYS.attemptToken)
  removeStorageValue(STORAGE_KEYS.authLoading)
  removeStorageValue(STORAGE_KEYS.authJob)
  removeStorageValue(STORAGE_KEYS.pendingRegistration)
}

export function mapScoreArrayToApiScores(scoreArray) {
  const [people, research, practical, aesthetic, extreme, economic] = scoreArray

  return {
    people_score: people ?? 0,
    research_score: research ?? 0,
    practical_score: practical ?? 0,
    aesthetic_score: aesthetic ?? 0,
    extreme_score: extreme ?? 0,
    economic_score: economic ?? 0,
  }
}
