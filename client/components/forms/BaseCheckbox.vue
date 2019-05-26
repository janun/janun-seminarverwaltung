<template>
  <label
    ref="label"
    :for="`check_${uuid}`"
    class="relative flex justify-start items-start cursor-pointer select-none"
  >
    <span class="w-5 h-5 block mr-4 relative flex-shrink-0">
      <input
        :id="`check_${uuid}`"
        ref="input"
        type="checkbox"
        :checked="isChecked"
        class="absolute inset-0 border-2 appearance-none block w-5 h-5"
        @change="onChange"
        @keydown.prevent.enter="$refs.input.click()"
      />

      <svg
        v-if="isChecked"
        class="text-green-500 absolute h-6 w-6 fill-current"
        style="right:-6px; top:-6px; left:0"
        viewBox="0 0 20 20"
      >
        <path d="M0 11l2-2 5 5L18 3l2 2L7 18z" />
      </svg>
    </span>

    <span>
      <slot>{{ label }}</slot>
    </span>
  </label>
</template>

<script>
import uuidMixin from '@/mixins/uuid.js'

export default {
  mixins: [uuidMixin],
  props: {
    value: { type: Boolean, default: false },
    label: { type: String, default: '' }
  },
  computed: {
    isChecked() {
      return this.value
    }
  },
  methods: {
    onChange(event) {
      this.$emit('input', event.target.checked)
    }
  }
}
</script>
