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

<script>
export default {
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
      this.$el.focus()
    },
    onInput(event) {
      if (this.validator && this.validator.$touch) {
        this.validator.$touch()
      }
      this.$emit('input', event.target.value)
    }
  }
}
</script>
