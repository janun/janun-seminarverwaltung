<template>
  <div
    class="flex flex-row-reverse justify-between bg-gray-100 p-5 rounded-b-lg mt-6"
  >
    <slot name="footer">
      <button
        class="btn btn-primary flex items-center"
        type="submit"
        :disabled="invalid"
      >
        {{ nextLabel }}
        <svg class="ml-2 fill-current h-3 w-3" viewBox="0 0 20 20">
          <path
            d="M16.172 9l-6.071-6.071 1.414-1.414L20 10l-.707.707-7.778 7.778-1.414-1.414L16.172 11H0V9z"
          />
        </svg>
      </button>
      <button
        type="button"
        class="btn btn-tertiary flex items-center"
        :disabled="prevDisabled"
        @click="$emit('prev')"
      >
        <svg class="mr-2 fill-current h-3 w-3" viewBox="0 0 20 20">
          <path
            d="M3.828 9l6.071-6.071-1.414-1.414L0 10l.707.707 7.778 7.778 1.414-1.414L3.828 11H20V9H3.828z"
          />
        </svg>
        {{ prevLabel }}
      </button>
    </slot>
  </div>
</template>

<script>
export default {
  props: {
    invalid: { type: Boolean, default: false },
    nextLabel: { type: String, default: 'Weiter' },
    prevLabel: { type: String, default: 'Zurück' },
    prevDisabled: { type: Boolean, default: false }
  }
}
</script>
