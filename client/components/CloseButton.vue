<template>
  <button
    type="button"
    class="h-12 w-12 rounded-full text-gray-600 focus:text-gray-900 hover:text-gray-900 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none flex items-center justify-center"
    v-on="$listeners"
  >
    <svg class="fill-current h-4 w-4" viewBox="0 0 512 512">
      <path
        d="M443.6 387.1L312.4 255.4l131.5-130c5.4-5.4 5.4-14.2 0-19.6l-37.4-37.6c-2.6-2.6-6.1-4-9.8-4-3.7 0-7.2 1.5-9.8 4L256 197.8 124.9 68.3c-2.6-2.6-6.1-4-9.8-4-3.7 0-7.2 1.5-9.8 4L68 105.9c-5.4 5.4-5.4 14.2 0 19.6l131.5 130L68.4 387.1c-2.6 2.6-4.1 6.1-4.1 9.8 0 3.7 1.4 7.2 4.1 9.8l37.4 37.6a13.78 13.78 0 0 0 19.6 0L256 313.1l130.7 131.1a13.78 13.78 0 0 0 19.6 0l37.4-37.6c2.6-2.6 4.1-6.1 4.1-9.8-.1-3.6-1.6-7.1-4.2-9.7z"
      />
    </svg>
  </button>
</template>

<script>
export default {
  methods: {
    focus() {
      this.$el.focus()
    }
  }
}
</script>
