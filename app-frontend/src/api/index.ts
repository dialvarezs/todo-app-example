import * as changeKeys from 'change-case/keys'

export const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

interface RequestInitWithJson extends RequestInit {
  json?: object | null | undefined
}

export async function apiFetch<T>(endpoint: string, options: RequestInitWithJson = {}): Promise<T> {
  if (options.json) {
    options.body = JSON.stringify(changeKeys.snakeCase(options.json, 5))
    options.json = undefined
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
  })

  const jsonResponse = await response.json()
  return changeKeys.camelCase(jsonResponse, 5) as T
}
