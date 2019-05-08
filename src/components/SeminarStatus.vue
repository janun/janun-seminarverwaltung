<template>
  <BaseSelect :value="value" :options="options" @input="onInput" />
</template>

<script lang="ts">
import Vue from 'vue';
import { Seminar } from '@/types.ts';
import BaseSelect from '@/components/BaseSelect.vue';
import { getNextStates } from '@/utils/status.ts';
import userMixin from '@/mixins/user.ts';

export default Vue.extend({
  components: {
    BaseSelect
  },
  mixins: [userMixin],
  props: {
    value: { type: String, required: true },
    seminar: { type: Object as () => Seminar, required: true }
  },
  computed: {
    options(): string[] {
      return [
        this.seminar.status,
        ...getNextStates(this.seminar.status, (this as any).isStaff as boolean)
      ];
    }
  },
  methods: {
    onInput(event: any) {
      this.$emit('input', event.target.value);
    }
  }
});
</script>
