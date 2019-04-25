<template>
  <transition name="modal">
    <div v-if="show" class="modal-backdrop" @click="close">
      <div class="modal mx-auto max-w-sm mt-8 card shadow-xl rounded-lg" role="dialog" @click.stop>
        <button
          type="button"
          class="float-right h-12 w-12 -mt-4 -mr-4 text-4xl rounded-full focus:outline-none focus:text-gray-900 hover:text-gray-900"
          @click="close"
        >
          &times;
        </button>
        <slot />
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import Vue from 'vue';
import { getFocusableChildren } from '@/utils/utils.ts';

export default Vue.extend({
  props: {
    focusEl: { type: Object as () => HTMLElement, default: null },
    show: { type: Boolean, default: false }
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
    // close on escape handler
    const escapeHandler = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && this.show) {
        event.stopPropagation();
        event.preventDefault();
        this.close();
      }
    };
    document.addEventListener('keydown', escapeHandler);
    this.$once('hook:destroyed', () => {
      document.removeEventListener('keydown', escapeHandler);
    });

    // trap focus handler
    const tabHandler = (event: KeyboardEvent) => {
      if (event.key === 'Tab' && this.show) {
        const els = getFocusableChildren(this.$el);
        const firstEl = els[0];
        const lastEl = els[els.length - 1];
        if (event.shiftKey && document.activeElement === firstEl) {
          lastEl.focus();
          event.preventDefault();
        } else if (document.activeElement === lastEl) {
          firstEl.focus();
          event.preventDefault();
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
      if (this.focusEl) {
        this.focusEl.focus();
      } else {
        const els = getFocusableChildren(this.$el);
        els[els.length > 1 ? 1 : 0].focus();
      }
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

/* modal transition */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.2s;
}

.modal {
  transition: all 0.2s;
}

.modal-enter .modal,
.modal-leave-to .modal {
  transform: scale(0.7);
}

.modal-enter,
.modal-leave-to {
  opacity: 0;
}
</style>
