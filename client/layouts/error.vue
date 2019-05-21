<template>
  <div class="mx-auto max-w-sm card border">
    <h1 class="text-red-500 font-bold text-xl mb-2">
      {{ title }}
    </h1>

    <p v-if="error.message">{{ error.message }}</p>

    <p class="mt-4 mb-2">Du kannst z.B. Folgendes versuchen:</p>
    <ul>
      <li class="mb-2">
        <a class="underline cursor-pointer" @click="reload">
          Seite neu laden
        </a>
      </li>
      <li>
        <a class="underline cursor-pointer" href="/">Zur Startseite</a>
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
      title: this.title
    }
  },
  computed: {
    title() {
      switch (this.error.statusCode) {
        case 404:
          return 'Seite nicht gefunden.'
        case 500:
          return 'Server Fehler'
        default:
          return 'Fehler'
      }
    }
  },
  methods: {
    reload() {
      location.reload(true)
    }
  }
}
</script>
