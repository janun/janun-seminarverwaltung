<template>
  <BaseDropdown class="inline-block">
    <button
      slot="trigger"
      type="button"
      class="flex items-center select-none input whitespace-no-wrap"
      :class="{ 'text-green-700': !allSelected }"
    >
      <span class="mr-1">{{ label }}:</span>
      <span v-if="allSelected">Alle</span>
      <span v-else class="truncate max-w-xs">{{ value.join(', ') }}</span>
      <svg class="fill-current h-4 w-4 ml-2" viewBox="0 0 20 20">
        <path
          d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"
        />
      </svg>
    </button>

    <BaseCheckbox
      v-for="option in options"
      :key="option"
      :value="value.includes(option)"
      :label="String(option)"
      class="whitespace-no-wrap my-1"
      role="listitem"
      @input="onInput(option, $event)"
    />
  </BaseDropdown>
</template>

<script>
import BaseCheckbox from '@/components/forms/BaseCheckbox.vue'
import BaseDropdown from '@/components/forms/BaseDropdown.vue'

export default {
  components: {
    BaseCheckbox,
    BaseDropdown
  },
  props: {
    label: { type: String, default: '' },
    value: { type: Array, default: () => [] },
    options: { type: Array, required: true }
  },
  computed: {
    allSelected() {
      return (
        this.value.length === 0 || this.value.length === this.options.length
      )
    }
  },
  methods: {
    onInput(option, isChecked) {
      let selected = [...this.value]
      if (isChecked) {
        selected.push(option)
      } else {
        selected = selected.filter(o => o !== option)
      }
      this.$emit('input', selected.sort())
    }
  }
}
</script>
