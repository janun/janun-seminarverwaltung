<template>
  <input
    class="shadow appearance-none border rounded py-2 px-3 text-gray-700 focus:outline-none focus:shadow-outline"
    :class="{ 'border-red-600': hasErrorsGetter() }"
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
    isValidGetter: { from: 'isValidGetter', default: () => () => false }
  },
  props: {
    type: { type: String, default: 'text' }
  },
  methods: {
    focus() {
      (this.$el as HTMLInputElement).focus();
    },
    onInput(event: Event) {
      this.$emit('input', (event.target as HTMLInputElement).value);
    }
  }
});
</script>
