// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxt/ui'],
  ssr:false,
  nitro: {
    preset: 'static'
  },
  app: {
    baseURL: '/settled_product/' 
  }
})