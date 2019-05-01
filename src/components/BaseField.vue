<template>
  <div class="mb-5">
    <label
      v-if="label || $slots.label"
      class="block mb-1 text-base text-gray-700"
      :class="{ 'text-red-600': hasErrors }"
      :for="childId"
    >
      <slot name="label">{{ label }}</slot>
      <span v-if="optional" class="text-sm text-gray-500 ml-1">(optional)</span>
    </label>

    <div v-if="helptext || $slots.helptext" class="text-sm -mt-1 mb-1">
      <slot name="helptext">{{ helptext }}</slot>
    </div>

    <slot />

    <div v-if="hasErrors" class="mt-1 text-red-600 font-bold text-sm italic">
      {{ firstErrorMessage }}
    </div>
    <div v-if="pending" class="spinner h-3 w-3"></div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import uuidMixin from '@/mixins/uuid.ts';
import { singleErrorExtractorMixin } from 'vuelidate-error-extractor';

export default Vue.extend({
  extends: singleErrorExtractorMixin,
  mixins: [uuidMixin],
  provide(): object {
    return {
      id: (this as any).childId,
      hasErrorsGetter: () => (this as any).hasErrors,
      isValidGetter: () => (this as any).isValid,
      validator: (this as any).preferredValidator
    };
  },
  props: {
    label: { type: String, default: '' },
    helptext: { type: String, default: '' },
    optional: { type: Boolean, default: false }
  },
  data: () => ({
    pending: false,
    pendingTimer: 0
  }),
  computed: {
    childId(): string {
      return `input_${(this as any).uuid}`;
    }
  },
  watch: {
    'preferredValidator.$pending'(pending: boolean) {
      if (this.pendingTimer) {
        clearTimeout(this.pendingTimer);
      }
      this.pendingTimer = setTimeout(() => {
        this.pending = pending;
      }, 100);
    }
  }
});
</script>
