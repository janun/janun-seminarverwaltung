<template>
  <select
    :id="id"
    :class="{ 'has-error': hasErrorsGetter() }"
    multiple
    class="w-full input"
    @input="onInput"
  >
    <option
      v-for="group in groups"
      :key="group.slug"
      :value="group.slug"
      :selected="value.includes(group.slug)"
    >
      {{ group.name }}
    </option>
  </select>
</template>

<script>
export default {
  props: {
    value: { type: Array, default: () => [] }
  },
  inject: {
    id: { from: 'id', default: null },
    hasErrorsGetter: { from: 'hasErrorsGetter', default: () => () => false },
    isValidGetter: { from: 'isValidGetter', default: () => () => false },
    validator: { from: 'validator', default: null }
  },
  computed: {
    groups() {
      return this.$store.state.groups.groups
    }
  },
  async created() {
    await this.$store.dispatch('groups/fetch')
  },
  methods: {
    onInput(event) {
      const selectedOption = event.target.selectedOptions
      const selected = Array.from(selectedOption).map(option => option.value)
      this.$emit('input', selected)
    }
  }
}
</script>
