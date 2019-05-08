<template>
  <span
    class="badge"
    :class="{
      'bg-green-200': stateInfo.color === 'green',
      'bg-red-200': stateInfo.color === 'red',
      'bg-yellow-200': stateInfo.color === 'yellow'
    }"
  >
    {{ value }}
  </span>
</template>

<script lang="ts">
import Vue from 'vue';
import { getStateInfo, StateInfo } from '../utils/status';

export default Vue.extend({
  props: {
    value: { type: String, required: true }
  },
  computed: {
    stateInfo(): StateInfo | undefined {
      return getStateInfo(this.value);
    }
  }
});
</script>
