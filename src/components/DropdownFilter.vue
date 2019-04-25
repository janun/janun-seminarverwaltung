<template>
  <BaseDropdown class="inline-block">
    <button
      type="button"
      slot="trigger"
      class="flex items-center select-none px-3 py-2 shadow border rounded whitespace-no-wrap bg-white  focus:shadow-outline"
      :class="{ 'text-green-500 font-bold': !allSelected }"
    >
      <span class="mr-1">{{ label }}:</span>
      <span v-if="allSelected">Alle</span>
      <span v-else class="truncate max-w-xs">{{ value.join(', ') }}</span>
      <svg class="fill-current h-4 w-4 ml-2" viewBox="0 0 20 20">
        <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
      </svg>
    </button>

    <BaseCheckbox
      v-for="option in options"
      :key="option"
      :value="value.includes(option)"
      :label="String(option)"
      @input="onInput(option, $event)"
      class="whitespace-no-wrap my-1"
      role="listitem"
    />
  </BaseDropdown>
</template>


<script lang="ts">
import Vue from 'vue';
import BaseCheckbox from '@/components/BaseCheckbox.vue';
import BaseDropdown from '@/components/BaseDropdown.vue';

export default Vue.extend({
  components: {
    BaseCheckbox,
    BaseDropdown
  },
  props: {
    label: { type: String, default: '' },
    value: { type: Array as () => string[] | number[], default: [] },
    options: { type: Array as () => string[] | number[], required: true }
  },
  computed: {
    allSelected(): boolean {
      return this.value.length === 0 || this.value.length === this.options.length;
    }
  },
  methods: {
    onInput(option: string | number, isChecked: boolean) {
      let selected = [...this.value];
      if (isChecked) {
        selected.push(option);
      } else {
        selected = selected.filter((o) => o !== option);
      }
      this.$emit('input', selected.sort());
    }
  }
});
</script>
