<template>
  <div class="base-form-section flex flex-wrap">
    <div class="w-full md:w-1/3">
      <h2 class="text-green-500 mb-5 font-bold text-lg">{{ label }}</h2>
      <slot name="description" />
    </div>

    <div class="w-full md:w-2/3">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    label: { type: String, required: true }
  }
}
</script>

<style lang="postcss">
.base-form-section + .base-form-section {
  @apply border-t pt-10;
}
.base-form-section:not(:last-of-type) {
  @apply pb-10;
}
</style>
