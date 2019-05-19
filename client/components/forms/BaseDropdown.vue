<template>
  <div
    class="relative"
    @keydown.down="onDown"
    @keydown.escape="onEscape"
    @keydown.up="onUp"
  >
    <div ref="trigger" role="button" aria-haspopup="true" @click="toggle">
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

<script>
import { getFocusableChildren } from '@/utils/dom.js'

export default {
  data: () => ({
    open: false
  }),
  mounted() {
    // close on click outside
    const clickOutsideHandler = event => {
      if (!this.$el.contains(event.target)) {
        this.open = false
      }
    }
    document.addEventListener('click', clickOutsideHandler)
    this.$once('hook:destroyed', () => {
      document.removeEventListener('click', clickOutsideHandler)
    })
  },
  methods: {
    toggle() {
      this.open = !this.open
    },
    onDown(event) {
      event.preventDefault()
      if (!this.open) {
        this.open = true
      } else {
        const els = getFocusableChildren(this.$refs.dropdownMenu)
        const currentIndex = Array.from(els).findIndex(
          el => el === document.activeElement
        )
        if (currentIndex === -1 || currentIndex === els.length - 1) {
          return els[0].focus()
        }
        els[currentIndex + 1].focus()
      }
    },
    onUp(event) {
      if (this.open) {
        event.preventDefault()
        const els = getFocusableChildren(this.$refs.dropdownMenu)
        const currentIndex = Array.from(els).findIndex(
          el => el === document.activeElement
        )
        if (currentIndex === 0) {
          return els[els.length - 1].focus()
        }
        els[currentIndex - 1].focus()
      }
    },
    onEscape(event) {
      if (this.open) {
        event.preventDefault()
        this.open = false
      }
    }
  }
}
</script>
