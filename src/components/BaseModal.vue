<template>
  <Portal to="modals">
    <div v-if="show" class="modal-backdrop md:p-8" @click="close">
      <div
        ref="modal"
        class="modal mx-auto max-w-lg mt-8 card shadow-xl rounded-lg"
        role="dialog"
        @click.stop
      >
        <button
          ref="closeButton"
          type="button"
          class="float-right h-12 w-12 -mt-4 -mr-4 text-4xl rounded-full focus:outline-none focus:text-gray-900 hover:text-gray-900"
          @click="close"
        >
          &times;
        </button>
        <slot />
      </div>
    </div>
  </Portal>
</template>

<script lang="ts">
import Vue from 'vue';
import { getFocusableChildren } from '@/utils/utils.ts';

export default Vue.extend({
  props: {
    show: { type: Boolean, required: true },
    closeOnEsc: { type: Boolean, default: true }
  },
  data: () => ({
    focusedBefore: null as HTMLElement | null
  }),
  watch: {
    show: {
      immediate: true,
      handler(show) {
        if (show) {
          document.body.classList.add('modal-open');
          setTimeout(() => {
            this.focus();
          });
          this.$emit('show');
        } else {
          document.body.classList.remove('modal-open');
          this.returnFocus();
        }
      }
    }
  },
  created() {
    // close on escape
    const escapeHandler = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && this.show && this.closeOnEsc) {
        event.stopPropagation();
        event.preventDefault();
        this.close();
      }
    };
    document.addEventListener('keydown', escapeHandler);
    this.$once('hook:destroyed', () => {
      document.removeEventListener('keydown', escapeHandler);
    });

    // trap focus
    const tabHandler = (event: KeyboardEvent) => {
      if (event.key === 'Tab' && this.show) {
        const els = getFocusableChildren(this.$refs.modal as Element);
        const firstEl = els[0];
        const lastEl = els[els.length - 1];
        if (event.shiftKey && document.activeElement === firstEl) {
          event.preventDefault();
          return lastEl.focus();
        }
        if (!event.shiftKey && document.activeElement === lastEl) {
          event.preventDefault();
          return firstEl.focus();
        }
      }
    };
    document.addEventListener('keydown', tabHandler);
    this.$once('hook:destroyed', () => {
      document.removeEventListener('keydown', tabHandler);
    });
  },
  methods: {
    close() {
      this.$emit('close');
    },
    focus() {
      this.focusedBefore = document.activeElement as HTMLElement;
      (this.$refs.closeButton as HTMLElement).focus();
    },
    returnFocus() {
      if (this.focusedBefore) {
        this.focusedBefore.focus();
        this.focusedBefore = null;
      }
    }
  }
});
</script>

<style lang="postcss">
.modal-open {
  overflow: hidden;
}

.modal-backdrop {
  @apply fixed overflow-auto p-2 inset-0 z-40;
  background: rgba(0, 0, 0, 0.7);
}
</style>
