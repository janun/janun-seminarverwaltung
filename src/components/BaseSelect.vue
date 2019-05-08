<template>
  <div class="relative">
    <select
      :id="id"
      ref="input"
      v-bind="$attrs"
      class="w-full input"
      :class="{ 'has-error': hasErrorsGetter() }"
      @input="onInput"
    >
      <slot>
        <option v-for="option in options" :key="option" :selected="option === value">
          {{ option }}
        </option>
      </slot>
    </select>

    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2">
      <svg class="fill-current h-4 w-4" viewBox="0 0 20 20">
        <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
      </svg>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  inheritAttrs: false,
  inject: {
    id: { from: 'id', default: null },
    hasErrorsGetter: { from: 'hasErrorsGetter', default: () => () => false },
    isValidGetter: { from: 'isValidGetter', default: () => () => false },
    validator: { from: 'validator', default: null }
  },
  props: {
    value: { type: String, default: '' },
    options: { type: Array as () => string[], default: () => [] }
  },
  methods: {
    onInput(event: Event) {
      const selected = (event.target as HTMLSelectElement).value;
      this.$emit('input', selected);
    }
  }
});
</script>
