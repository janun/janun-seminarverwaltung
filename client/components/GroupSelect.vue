<template>
  <BaseSelect @input="onInput">
    <option v-if="emptyIsPossible" :value="''" :selected="!value">
      - keine -
    </option>
    <option
      v-for="group in groups"
      :key="group.slug"
      :value="group.slug"
      :selected="group.slug === value"
    >
      {{ group.name }}
    </option>
  </BaseSelect>
</template>

<script>
import BaseSelect from '@/components/forms/BaseSelect.vue'

export default {
  components: {
    BaseSelect
  },
  props: {
    value: { type: [String, Number], default: '' },
    emptyIsPossible: { type: Boolean, default: true },
    possibleGroups: { type: Array, default: undefined }
  },
  data: () => ({
    groups: []
  }),
  async created() {
    if (this.possibleGroups) {
      this.groups = this.possibleGroups
    } else {
      await this.$store.dispatch('groups/fetch')
      this.groups = this.$store.state.groups.groups
    }
  },
  methods: {
    onInput(value) {
      this.$emit('input', value)
    }
  }
}
</script>
