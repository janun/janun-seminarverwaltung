<template>
  <div class="relative flex items-center">
    <BaseInput v-bind="$attrs" :type="type" class="w-full" @input="onInput" />
    <button
      type="button"
      class="absolute right-0 p-2 mr-1 rounded-full focus:outline-none focus:shadow-outline"
      @click="show = !show"
    >
      <svg class="fill-current h-4 w-4" viewBox="0 0 20 20">
        <path
          v-if="show"
          d="M12.81 4.36l-1.77 1.78a4 4 0 0 0-4.9 4.9l-2.76 2.75C2.06 12.79.96 11.49.2 10a11 11 0 0 1 12.6-5.64zm3.8 1.85c1.33 1 2.43 2.3 3.2 3.79a11 11 0 0 1-12.62 5.64l1.77-1.78a4 4 0 0 0 4.9-4.9l2.76-2.75zm-.25-3.99l1.42 1.42L3.64 17.78l-1.42-1.42L16.36 2.22z"
        />
        <path
          v-else
          d="M.2 10a11 11 0 0 1 19.6 0A11 11 0 0 1 .2 10zm9.8 4a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm0-2a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"
        />
      </svg>
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      show: false
    }
  },
  computed: {
    type() {
      return this.show ? 'text' : 'password'
    }
  },
  methods: {
    focus() {
      this.$el.focus()
    },
    onInput(value) {
      this.$emit('input', value)
    }
  }
}
</script>
