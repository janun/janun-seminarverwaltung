<template>
  <textarea
    :id="id"
    ref="textarea"
    :class="{ 'has-errors': hasErrorsGetter() }"
    v-bind="{ rows: 5, ...$attrs }"
    v-on="{ ...$listeners, input: onInput }"
  ></textarea>
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
  mounted() {
    this.resizeTextarea();
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
      this.resizeTextarea();
    },
    resizeTextarea() {
      const el = this.$el as HTMLInputElement;
      el.style.setProperty('height', 'auto'); // needed to get correct values
      el.style.setProperty('height', `${el.scrollHeight + el.offsetHeight - el.clientHeight}px`);
    }
  }
});
</script>

<style lang="postcss" scoped>
textarea {
  @apply w-full appearance-none rounded py-2 px-3 leading-tight resize-none -mb-2 bg-gray-20 border border-gray-400;
}

textarea:focus {
  @apply outline-none shadow-outline;
}

.has-errors {
  @apply border-red-600;
}
</style>
