<template>
  <textarea
    class="w-full shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline resize-none -mb-2"
    :class="{ 'border-red-600': hasErrorsGetter() }"
    :id="id"
    ref="textarea"
    v-bind="$attrs"
    v-on="{ ...$listeners, input: onInput }"
    rows="5"
  ></textarea>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  inject: {
    id: { from: 'id', default: null },
    hasErrorsGetter: { from: 'hasErrorsGetter', default: () => () => false },
    isValidGetter: { from: 'isValidGetter', default: () => () => false }
  },
  methods: {
    focus() {
      (this.$el as HTMLInputElement).focus();
    },
    onInput(event: Event) {
      this.$emit('input', (event.target as HTMLInputElement).value);
      this.resizeTextarea();
    },
    resizeTextarea() {
      const el = this.$el as HTMLInputElement;
      el.style.setProperty('height', 'auto'); // needed to get correct values
      el.style.setProperty('height', `${el.scrollHeight + el.offsetHeight - el.clientHeight}px`);
    }
  },
  mounted() {
    this.resizeTextarea();
  }
});
</script>
