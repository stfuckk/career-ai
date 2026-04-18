import { readCurrentUser } from '@/lib/api'
import { STORAGE_KEYS, clearAuthStorage, readStorageValue, writeStorageJson } from '@/lib/storage'

let authValidationPromise = null

export function hasPersistedAuth() {
  return readStorageValue(STORAGE_KEYS.authFlag) === 'true' || Boolean(readStorageValue(STORAGE_KEYS.accessToken))
}

export function clearInvalidSession() {
  clearAuthStorage()
}

export async function validatePersistedSession() {
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
