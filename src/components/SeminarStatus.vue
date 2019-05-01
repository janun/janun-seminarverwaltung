<template>
  <BaseSelect :value="value" :options="options" @input="onInput" />
</template>

<script lang="ts">
import Vue from 'vue';
import { Seminar } from '@/types.ts';
import BaseSelect from '@/components/BaseSelect.vue';
import { getNextStates } from '@/utils/status.ts';

export default Vue.extend({
  components: {
    BaseSelect
  },
  props: {
    value: { type: String, required: true },
    seminar: { type: Object as () => Seminar, required: true }
  },
  computed: {
    options(): string[] {
      return [this.seminar.status, ...getNextStates(this.seminar.status)];
    }
  },
  methods: {
    onInput(event: any) {
      this.$emit('input', event.target.value);
    }
  }
});
</script>
