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
      :key="group.pk"
      :value="group.pk"
      :selected="value.includes(group.pk)"
    >
      {{ group.name }}
    </option>
  </select>
</template>

<script lang="ts">
import Vue from 'vue';

interface Group {
  pk: number;
  name: string;
}

export default Vue.extend({
  props: {
    value: { type: Array as () => string[], default: () => [] }
  },
  inject: {
    id: { from: 'id', default: null },
    hasErrorsGetter: { from: 'hasErrorsGetter', default: () => () => false },
    isValidGetter: { from: 'isValidGetter', default: () => () => false },
    validator: { from: 'validator', default: null }
  },
  data: () => ({
    groups: [] as Group[]
  }),
  async created() {
    this.groups = await this.$store.dispatch('groups/getGroupNames');
  },
  methods: {
    onInput(event: Event) {
      const selectedOption = (event.target as HTMLSelectElement).selectedOptions;
      const selected = Array.from(selectedOption).map((option) => option.value);
      this.$emit('input', selected);
    }
  }
});
</script>
