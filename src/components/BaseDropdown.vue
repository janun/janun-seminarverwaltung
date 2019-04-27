<template>
  <div class="relative" @keydown.down="onDown" @keydown.escape="onEscape" @keydown.up="onUp">
    <div role="button" ref="trigger" @click="toggle" aria-haspopup="true">
      <slot name="trigger" />
    </div>

    <transition name="fade">
      <div
        v-show="open"
        ref="dropdownMenu"
        class="absolute bottom-0 left-0 bg-white border py-2 px-4 rounded z-20 shadow-lg min-w-full"
        style="transform: translateY(100%)"
        :aria-hidden="!open"
      >
        <div role="list">
          <slot />
        </div>
      </div>
    </transition>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { getFocusableChildren } from '../utils/utils';

export default Vue.extend({
  data: () => ({
    open: false
  }),
  methods: {
    toggle() {
      this.open = !this.open;
    },
    onDown(event: Event) {
      event.preventDefault();
      if (!this.open) {
        this.open = true;
      } else {
        const els = getFocusableChildren(this.$refs.dropdownMenu as Element);
        const currentIndex = Array.from(els).findIndex((el) => el === document.activeElement);
        if (currentIndex === -1 || currentIndex === els.length - 1) {
          return els[0].focus();
        }
        els[currentIndex + 1].focus();
      }
    },
    onUp(event: Event) {
      if (this.open) {
        event.preventDefault();
        const els = getFocusableChildren(this.$refs.dropdownMenu as Element);
        const currentIndex = Array.from(els).findIndex((el) => el === document.activeElement);
        if (currentIndex === 0) {
          return els[els.length - 1].focus();
        }
        els[currentIndex - 1].focus();
      }
    },
    onEscape(event: Event) {
      if (this.open) {
        event.preventDefault();
        this.open = false;
      }
    }
  },
  created() {
    // close on click outside
    const clickOutsideHandler = (event: Event) => {
      if (!this.$el.contains(event.target as Node)) {
        this.open = false;
      }
    };
    document.addEventListener('click', clickOutsideHandler);
    this.$once('hook:destroyed', () => {
      document.removeEventListener('click', clickOutsideHandler);
    });
  }
});
</script>