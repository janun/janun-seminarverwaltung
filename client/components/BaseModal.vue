<template>
  <Portal to="modals">
    <transition name="modal">
      <div
        v-if="show"
        class="modal-backdrop md:p-5"
        @click="close"
        @keydown.esc.stop="close"
      >
        <div
          ref="modal"
          aria-modal="true"
          tabindex="-1"
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
    </transition>
  </Portal>
</template>

<script>
import { getFocusableChildren } from '@/utils/dom.js'

export default {
  props: {
    show: { type: Boolean, required: true },
    closeOnEsc: { type: Boolean, default: true }
  },
  data: () => ({
    focusedBefore: null
  }),
  watch: {
    show(show) {
      if (show) {
        document.body.classList.add('modal-open')
        this.$once('hook:destroyed', () => {
          document.body.classList.remove('modal-open')
        })
        setTimeout(() => {
          this.focus()
        })
        this.$emit('show')
      } else {
        document.body.classList.remove('modal-open')
        this.returnFocus()
      }
    }
  },
  mounted() {
    // trap focus
    const tabHandler = event => {
      if (event.key === 'Tab' && this.show) {
        const els = getFocusableChildren(this.$refs.modal)
        const firstEl = els[0]
        const lastEl = els[els.length - 1]
        if (event.shiftKey && document.activeElement === firstEl) {
          event.preventDefault()
          return lastEl.focus()
        }
        if (!event.shiftKey && document.activeElement === lastEl) {
          event.preventDefault()
          return firstEl.focus()
        }
      }
    }
    document.addEventListener('keydown', tabHandler)
    this.$once('hook:destroyed', () => {
      document.removeEventListener('keydown', tabHandler)
    })
  },
  methods: {
    close() {
      this.$emit('close')
    },
    focus() {
      this.focusedBefore = document.activeElement
      this.$refs.closeButton.focus()
    },
    returnFocus() {
      if (this.focusedBefore) {
        this.focusedBefore.focus()
        this.focusedBefore = null
      }
    }
  }
}
</script>

<style lang="postcss">
.modal-open {
  overflow: hidden;
}

.modal-backdrop {
  @apply fixed overflow-auto p-2 inset-0 z-40;
  background: rgba(0, 0, 0, 0.6);
}

/* modal transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s linear;
}

.modal {
  transition: transform 0.3s;
}

.modal-enter .modal,
.modal-leave-to .modal {
  transform: translateY(-300px);
}

.modal-enter,
.modal-leave-to {
  opacity: 0;
}
</style>
