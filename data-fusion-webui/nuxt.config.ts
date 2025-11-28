/* eslint-disable nuxt/nuxt-config-keys-order */
// https://nuxt.com/docs/api/configuration/nuxt-config
import process from 'node:process'

export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@vueuse/nuxt'
  ],

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  routeRules: {
    '/api/**': {
      cors: true
    }
  },

  compatibilityDate: '2024-07-11',

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  },

  imports: {
    dirs: ['server/utils']
  },

  runtimeConfig: {
    platformApiBaseUrl: process.env.PLATFORM_API_BASE_URL ?? 'http://localhost:8000',
    platformApiKey: process.env.PLATFORM_API_KEY ?? '',
    public: {
      platformApiBaseUrl: process.env.NUXT_PUBLIC_PLATFORM_API_BASE_URL ?? process.env.PLATFORM_API_BASE_URL ?? 'http://localhost:8000'
    }
  }
})
