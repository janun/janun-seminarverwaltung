<template>
  <form @submit.prevent="$emit('submit', $event)">
    <slot />
  </form>
</template>

<script lang="ts">
import Vue from 'vue';
import { Validation } from 'vuelidate';

export default Vue.extend({
  props: {
    validator: { type: Object as () => object, default: () => ({}) }
  },
  provide(): object {
    return {
      formValidator: this.validator
    };
  }
});
</script>
