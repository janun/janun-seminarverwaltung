<template>
  <div class="mb-5">
    <label
      v-if="label || $slots.label"
      class="block mb-1 text-sm text-gray-700 font-bold"
      :class="{ 'text-red-600': hasErrors }"
      :for="childId"
    >
      <slot name="label">{{ label }}</slot>
      <span v-if="optional" class="text-xs text-gray-600 ml-1 font-normal">
        optional
      </span>
    </label>

    <div
      v-if="helptext || $slots.helptext"
      class="text-sm -mt-1 mb-1 text-gray-600"
    >
      <slot name="helptext">{{ helptext }}</slot>
    </div>

    <slot />

    <div
      v-if="hasErrors || serverErrorMessages"
      class="mt-1 text-red-600 font-bold text-sm italic"
    >
      {{ firstErrorMessage }}
      <div v-for="error in serverErrorMessages" :key="error">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import uuidMixin from '@/mixins/uuid.js'
import { singleErrorExtractorMixin } from 'vuelidate-error-extractor'

export default {
  extends: singleErrorExtractorMixin,
  mixins: [uuidMixin],
  inject: {
    serverErrorsGetter: {
      default: () => () => {}
    }
  },
  provide() {
    return {
      id: this.childId,
      hasErrorsGetter: () => this.hasErrors,
      isValidGetter: () => this.isValid,
      validator: this.preferredValidator
    }
  },
  props: {
    label: { type: String, default: '' },
    helptext: { type: String, default: '' },
    optional: { type: Boolean, default: false }
  },
  computed: {
    childId() {
      return `input_${this.uuid}`
    },
    serverErrorMessages() {
      const serverErrors = this.serverErrorsGetter()
      if (this.name && serverErrors) {
        return serverErrors[this.name]
      }
      return null
    }
  }
}
</script>
