// https://nuxt.com/docs/guide/recipes/custom-usefetch#custom-usefetchuseasyncdata

import type { UseFetchOptions } from "nuxt/app"

export function useApiFetch<T>(
  url: string | (() => string),
  options?: UseFetchOptions<T>
) {
  return useFetch(url, {
    ...options,
    $fetch: useNuxtApp().$api as typeof $fetch,
  })
}
