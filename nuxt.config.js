import pkg from './package'

export default {
  mode: 'spa',

  srcDir: 'client/',

  /*
   ** Headers of the page
   */
  head: {
    title: '',
    titleTemplate: titleChunk =>
      titleChunk ? `JANUN Seminare - ${titleChunk}` : 'JANUN Seminare',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: pkg.description }
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
  },

  manifest: {
    name: 'JANUN Seminarverwaltung',
    lang: 'de'
  },

  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#3a9d00', continuous: true },

  /*
   ** Global CSS
   */
  css: ['~/assets/css/tailwind.css', 'typeface-cabin'],

  /*
   ** Plugins to load before mounting the App
   */
  plugins: [
    '@/plugins/vuelidate',
    '@/plugins/vuelidateErrorExtractor',
    '@/plugins/portalVue',
    '@/plugins/globalComponents',
    '@/plugins/formatters',
    '@/plugins/toast',
    '@/plugins/axios'
  ],

  /*
   ** Nuxt.js modules
   */
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/proxy',
    '@nuxtjs/auth',
    '@nuxtjs/pwa',
    'nuxt-purgecss',
    'nuxt-compress'
  ],

  /*
   ** Proxy config for development
   */
  proxy: {
    '/api': {
      target: 'http://localhost:8000'
    }
  },

  /*
   ** Axios module configuration
   */
  axios: {
    baseURL: '/api',
    retry: true
  },

  /*
   ** Auth module settings
   */
  auth: {
    redirect: {
      logout: '/login'
    },
    strategies: {
      local: {
        endpoints: {
          login: {
            url: 'auth/login/',
            method: 'post',
            propertyName: 'key'
          },
          user: { url: 'auth/user/', method: 'get', propertyName: '' },
          logout: { url: 'auth/logout/', method: 'post' }
        },
        tokenType: 'Token'
      }
    }
  },

  /*
   ** router config
   */
  router: {
    middleware: ['auth'] // require authentication everywhere
  },

  purgeCSS: {
    paths: ['nuxt.config.js']
  },

  /*
   ** Build configuration
   */
  build: {
    postcss: {
      plugins: [require('tailwindcss'), require('autoprefixer')]
    },

    extractCSS: true,
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {
      // Run ESLint on save
      if (ctx.isDev && ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    }
  }
}
