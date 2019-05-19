<template>
  <div class="toaster">
    <transition-group name="appear">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="{ 'bg-red-600': toast.type === 'error' }"
      >
        {{ toast.text }}
      </div>
    </transition-group>
  </div>
</template>

<script>
export default {
  computed: {
    toasts() {
      return this.$store.state.toasts.toasts
    }
  }
}
</script>

<style lang="postcss">
.toaster {
  @apply fixed z-50 top-0 mt-2 flex flex-row justify-center w-full select-none pointer-events-none;
}

.toast {
  @apply text-white px-5 py-2 my-2 rounded-lg shadow;
  background-color: rgba(10, 10, 10, 0.9);
}

@screen md {
  .toast {
    text-align: center;
    min-width: 200px;
  }
}

/* fade */
.appear-enter-active,
.appear-leave-active {
  transition: transform 250ms ease-in-out;
}

.appear-enter,
.appear-leave-to {
  transform: translateY(-100px);
}
</style>
