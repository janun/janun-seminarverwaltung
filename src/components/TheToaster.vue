<template>
  <div
    class="fixed z-50 bottom-0 mb-10 flex flex-row justify-center w-full select-none pointer-events-none"
  >
    <transition-group name="fade">
      <div
        class="text-white px-5 py-2 my-2 opacity-75 rounded-full shadow-xl"
        v-for="toast in toasts"
        :key="toast.id"
        :class="{ 'bg-black': !toast.type, 'bg-red-500': toast.type === 'error' }"
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
