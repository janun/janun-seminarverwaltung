<template>
  <div class="toaster">
    <transition-group name="fade">
      <div
        class="toast"
        v-for="toast in toasts"
        :key="toast.id"
        :class="{ 'bg-red-600': toast.type === 'error' }"
      >
        {{ toast.text }}
      </div>
    </transition-group>
  </div>
</template>


<script lang="ts">
import Vue from 'vue';
import { Toast } from '@/types.ts';

export default Vue.extend({
  computed: {
    toasts(): Toast[] {
      return this.$store.getters['toasts/all'];
    }
  }
});
</script>

<style lang="postcss">
.toaster {
  @apply fixed z-50 bottom-0 mb-10 flex flex-row justify-center w-full select-none pointer-events-none;
}

.toast {
  @apply text-white px-5 py-2 my-2 rounded-full shadow-xl;
  background-color: rgba(10, 10, 10, 0.9);
}
</style>
