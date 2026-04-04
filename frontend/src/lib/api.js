const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1'

function normalizeErrorPayload(payload, response) {
  if (payload?.detail && Array.isArray(payload.detail)) {
    const fieldErrors = {}

    for (const item of payload.detail) {
      const fieldName = item.loc?.[item.loc.length - 1]

      if (typeof fieldName === 'string') {
        fieldErrors[fieldName] = item.msg
      }
    }

    return {
      message: payload.detail[0]?.msg ?? 'Ошибка валидации.',
      fieldErrors,
      status: response.status,
    }
  }

  if (typeof payload?.detail === 'string') {
    return {
      message: payload.detail,
      fieldErrors: {},
      status: response.status,
    }
  }

  return {
    message: 'Не удалось выполнить запрос.',
    fieldErrors: {},
    status: response.status,
  }
}

async function apiRequest(path, { method = 'GET', body, token } = {}) {
  const headers = {}

  if (body !== undefined) {
    headers['Content-Type'] = 'application/json'
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })

  const text = await response.text()
  const payload = text ? JSON.parse(text) : null

  if (!response.ok) {
    throw normalizeErrorPayload(payload, response)
  }

  return payload
}

export function submitAnonymousTest(scores) {
  return apiRequest('/test-attempts/submit-anonymous', {
    method: 'POST',
    body: { scores },
  })
}

export function registerUser(payload) {
  return apiRequest('/auth/register', {
    method: 'POST',
    body: payload,
  })
}

export function loginUser(payload) {
  return apiRequest('/auth/token', {
    method: 'POST',
    body: payload,
  })
}

export function readLatestTestResult(token) {
  return apiRequest('/users/me/latest-test-result', { token })
}

export function readAiJobStatus(jobId) {
  return apiRequest(`/ai-jobs/${jobId}/status`)
}

export function readAiJobResult(jobId) {
  return apiRequest(`/ai-jobs/${jobId}/result`)
}
