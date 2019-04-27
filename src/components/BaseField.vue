<template>
  <div class="mb-6">
    <label
      class="block mb-1 text-base text-gray-700"
      :class="{ 'text-red-600': hasErrors }"
      :for="childId"
      v-if="label || $slots.label"
    >
      <slot name="label">{{ label }}</slot>
    </label>

    <div v-if="helptext || $slots.helptext" class="text-sm -mt-1 mb-1">
      <slot name="helptext">{{ helptext }}</slot>
    </div>

    <slot />

    <div class="ml-1 mt-1 text-red-600 font-bold text-sm italic">{{ firstErrorMessage }}</div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import uuidMixin from '@/mixins/uuid.ts';
import { singleErrorExtractorMixin } from 'vuelidate-error-extractor';

export default Vue.extend({
  extends: singleErrorExtractorMixin,
  mixins: [uuidMixin],
  provide() {
    return {
      id: (this as any).childId,
      hasErrorsGetter: () => (this as any).hasErrors,
      isValidGetter: () => (this as any).isValid,
      validator: (this as any).preferredValidator
    };
  },
  props: {
    label: { type: String, default: '' },
    helptext: { type: String, default: '' }
  },
  computed: {
    childId(): string {
      return `input_${(this as any).uuid}`;
    },
    hasFocus() {
      this.$el.contains(document.activeElement);
    }
  }
});
</script>
