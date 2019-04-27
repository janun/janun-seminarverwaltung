<template>
  <input
    :class="{ 'has-error': hasErrorsGetter() }"
    :type="type"
    :id="id"
    v-bind="$attrs"
    @input="onInput"
  />
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  inject: {
    id: { from: 'id', default: null },
    hasErrorsGetter: { from: 'hasErrorsGetter', default: () => () => false },
    isValidGetter: { from: 'isValidGetter', default: () => () => false },
    validator: { from: 'validator', default: null }
  },
  props: {
    type: { type: String, default: 'text' }
  },
  methods: {
    focus() {
      (this.$el as HTMLInputElement).focus();
    },
    onInput(event: Event) {
      if ((this as any).validator && (this as any).validator.$touch) {
        (this as any).validator.$touch();
      }
      this.$emit('input', (event.target as HTMLInputElement).value);
    }
  }
});
</script>

<style lang="postcss" scoped>
input {
  @apply appearance-none border border-gray-400 rounded py-2 px-3 bg-gray-20;
}

input:focus {
  @apply outline-none shadow-outline;
}

input.has-error {
  @apply border-red-600;
}
</style>
