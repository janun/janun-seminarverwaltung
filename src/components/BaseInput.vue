<template>
  <input
    :id="id"
    class="input"
    :class="{ 'has-error': hasErrorsGetter() }"
    :type="type"
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
