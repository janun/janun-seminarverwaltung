<template>
  <form @submit.prevent="$emit('submit', $event)">
    <slot />
  </form>
</template>

<script>
export default {
  props: {
    validator: { type: Object, default: () => ({}) }
  },
  provide() {
    return {
      formValidator: this.validator
    }
  }
}
</script>
