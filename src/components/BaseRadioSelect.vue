<template>
  <div>
    <label
      class="relative select-none px-4 py-2 inline-block border-2 border-transparent rounded-lg my-1 bg-white pl-10"
      :class="[
        checked ? 'shadow-none border-green-500' : 'shadow hover:shadow-md',
        disabled ? 'cursor-not-allowed text-gray-500' : 'cursor-pointer focus-within:shadow-outline'
      ]"
    >
      <span
        class="absolute flex justify-center items-center h-4 w-4 rounded-full border-2 ml-3 mt-3 top-0 left-0"
        :class="[checked ? 'border-green-500' : '']"
      >
        <span v-if="checked" class="h-2 w-2 rounded-full bg-green-500" />
      </span>

      <input
        class="opacity-0 absolute h-0 w-0 cursor-pointer"
        type="radio"
        :value="valueIfChecked"
        :checked="checked"
        :disabled="disabled"
        @change="$emit('input', valueIfChecked)"
      />

      <slot>{{ label }}</slot>
    </label>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: {
    valueIfChecked: { type: [String, Boolean], required: true },
    value: { type: [String, Boolean], default: '' },
    disabled: { type: Boolean, default: false },
    label: { type: String, default: '' }
  },
  computed: {
    checked(): boolean {
      return this.valueIfChecked === this.value;
    }
  }
});
</script>
