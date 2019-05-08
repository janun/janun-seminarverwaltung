<template>
  <BaseSelect @input="onInput">
    <option v-if="emptyIsPossible" :value="''" :selected="!value">
      - keine -
    </option>
    <option
      v-for="group in groups"
      :key="group.pk"
      :value="group.pk"
      :selected="group.pk === value"
    >
      {{ group.name }}
    </option>
  </BaseSelect>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseSelect from '@/components/BaseSelect.vue';

interface Group {
  pk: string;
  name: string;
}

export default Vue.extend({
  components: {
    BaseSelect
  },
  props: {
    value: { type: [String, Number], default: '' },
    emptyIsPossible: { type: Boolean, default: true },
    possibleGroups: { type: Array as () => Group[] | undefined, default: undefined }
  },
  data: () => ({
    groups: [] as Group[]
  }),
  async created() {
    if (this.possibleGroups) {
      this.groups = this.possibleGroups;
    } else {
      this.groups = await this.$store.dispatch('groups/getGroupNames');
    }
  },
  methods: {
    onInput(value: string) {
      this.$emit('input', value);
    }
  }
});
</script>
