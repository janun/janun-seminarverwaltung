<template>
  <div class="relative inline-block">
    <select
      ref="input"
      v-bind="$attrs"
      class="block appearance-none w-full border border-gray-400 py-2 px-4 pr-8 rounded bg-gray-20 focus:outline-none focus:shadow-outline"
      :class="innerClass"
      v-on="$listeners"
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
  props: {
    value: { type: String, default: '' },
    innerClass: { tyspe: String, default: '' },
    options: {
      type: Array as () => string[],
      default: () => [],
      validator: (options: any[]) => options.every((opt) => typeof opt === 'string')
    }
  }
});
</script>
