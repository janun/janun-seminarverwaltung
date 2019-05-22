<template>
  <div class="mx-auto max-w-sm text-center">
    <h1 class="text-gray-900 font-bold text-2xl mb-2">
      {{ title }}
    </h1>

    <p v-if="message">{{ message }}</p>

    <p class="mt-6 mb-4 text-gray-600">Du kannst z.B. Folgendes versuchen:</p>
    <ul>
      <li v-if="![404, 403].includes(error.statusCode)" class="mb-2">
        <button class="btn btn-outline" @click="reload">
          Seite neu laden
        </button>
      </li>
      <li class="mb-2">
        <button class="btn btn-outline" @click="back">
          Geh zurück
        </button>
      </li>
      <li>
        <a class="btn btn-outline" href="/">Zur Startseite</a>
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
  layout: 'default',
  head() {
    return {
      title: this.title
    }
  },
  computed: {
    title() {
      switch (this.error.statusCode) {
        case 404:
          return 'Seite nicht gefunden.'
        case 403:
          return 'Keine Berechtigung.'
        case 500:
          return 'Server Fehler'
        default:
          return 'Fehler'
      }
    },
    message() {
      switch (this.error.statusCode) {
        case 404:
          return 'Diese Seite wurde nicht gefunden. Vielleicht hast du auch keine Berechtigung sie zu sehen.'
        case 403:
          return 'Du hast keine Berechtigung diese Seite zu sehen oder diese Aktion auszuführen.'
        case 500:
          return 'Auf dem Server ist ein Fehler passiert.'
        default:
          return this.error.message
      }
    }
  },
  methods: {
    reload() {
      location.reload(true)
    },
    back() {
      this.$router.go(-1)
    }
  }
}
</script>
