<template>
  <div class="mx-auto max-w-sm card border">
    <h1 class="text-red-500 font-bold text-xl mb-5">
      <span v-if="statusCode === 404">
        Hmm, Seite nicht gefunden
      </span>
      <span v-else>
        Upps, Ein Fehler ist aufgetreten
      </span>
    </h1>
    <ul>
      <li class="my-3">
        <a class="link cursor-pointer" @click="$router.go(-1)">Zurück</a>
      </li>
      <li class="my-3">
        <nuxt-link class="link" to="/">Zur Startseite</nuxt-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'NuxtError',
  props: {
    error: { type: Object, default: null }
  },
  layout: 'empty',
  head() {
    return {
      title: this.message,
      meta: [
        {
          name: 'viewport',
          content:
            'width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no'
        }
      ]
    }
  },
  computed: {
    statusCode() {
      return (this.error && this.error.statusCode) || 500
    },
    message() {
      return this.error.message || 'Fehler'
    }
  }
}
</script>
