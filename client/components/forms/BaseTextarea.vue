<template>
  <textarea
    :id="id"
    ref="textarea"
    class="w-full input resize-none"
    :class="{ 'has-errors': hasErrorsGetter() }"
    v-bind="{ rows: 5, ...$attrs }"
    v-on="{ ...$listeners, input: onInput }"
  ></textarea>
</template>

<script>
export default {
  inject: {
    id: { from: 'id', default: null },
    hasErrorsGetter: { from: 'hasErrorsGetter', default: () => () => false },
    isValidGetter: { from: 'isValidGetter', default: () => () => false },
    validator: { from: 'validator', default: null }
  },
  mounted() {
    this.resizeTextarea()
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
      this.resizeTextarea()
    },
    resizeTextarea() {
      const el = this.$el
      el.style.setProperty('height', 'auto') // needed to get correct values
      el.style.setProperty(
        'height',
        `${el.scrollHeight + el.offsetHeight - el.clientHeight}px`
      )
    }
  }
}
</script>
