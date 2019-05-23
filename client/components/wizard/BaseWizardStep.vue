<template>
  <div
    v-if="active"
    :key="title"
    class="w-full max-w-3xl rounded-lg bg-white shadow-md p-5"
  >
    <div class="flex items-center border-b -mx-5 px-5 pb-5 mb-4">
      <h1 class="text-lg font-bold text-green-500">
        {{ wizardTitleGetter() }}
        <span class="ml-2 text-gray-600 text-sm font-normal">
          {{ currentIndex + 1 }} / {{ steps.length }}
        </span>
      </h1>
      <button
        class="-mr-1 ml-auto hover:bg-gray-200 focus:bg-gray-200 focus:shadow-outline rounded-full p-3 outline-none"
        title="Abbrechen"
        @click="cancel"
      >
        <svg class="fill-current text-gray-700 w-3 h-3" viewBox="0 0 20 20">
          <path
            d="M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z"
          />
        </svg>
      </button>
    </div>

    <form @submit.prevent="submit">
      <div class="flex">
        <div>
          <BaseWizardNav
            class="hidden md:block mr-12 px-3 mb-4 bg-gray-100 rounded shadow"
          />
        </div>
        <div ref="content">
          <slot />
        </div>
      </div>

      <BaseWizardFooter
        class="-mx-5 -mb-5"
        :prev-label="prevLabel"
        :next-label="nextLabel"
        :invalid="invalid"
        :prev-disabled="prevDisabled"
        @prev="onPrev"
      />
    </form>
  </div>
</template>

<script>
import { getFocusableChildren } from '@/utils/dom.js'
import BaseWizardNav from '@/components/wizard/BaseWizardNav.vue'
import BaseWizardFooter from '@/components/wizard/BaseWizardFooter.vue'

export default {
  inject: [
    'next',
    'prev',
    'currentIndexGetter',
    'stepsGetter',
    'wizardTitleGetter',
    'cancel'
  ],
  components: {
    BaseWizardNav,
    BaseWizardFooter
  },
  props: {
    title: { type: String, required: true }, // used by BaseWizardNav
    v: { type: Object, default: null },
    nextLabel: { type: String, default: 'Weiter' },
    prevLabel: { type: String, default: 'Zurück' },
    prevDisabled: { type: Boolean, default: false }
  },
  provide() {
    return {
      formValidator: this.v
    }
  },
  data: () => ({
    active: false, // set by parent
    visited: false
  }),
  computed: {
    valid() {
      return !this.v || !this.v.$invalid
    },
    invalid() {
      return this.v && this.v.$invalid
    },
    currentIndex() {
      return this.currentIndexGetter()
    },
    steps() {
      return this.stepsGetter()
    }
  },
  watch: {
    active: {
      immediate: true,
      handler(active) {
        if (active) {
          this.visited = true
          this.focus()
        }
      }
    }
  },
  methods: {
    submit() {
      this.$emit('submit')
      this.next()
    },
    onPrev() {
      this.$emit('prev')
      this.prev()
    },
    focus() {
      this.$nextTick(() => {
        const focusEls = getFocusableChildren(this.$refs.content)
        if (focusEls.length) {
          focusEls[0].focus()
        }
      })
    }
  }
}
</script>

<style lang="postcss">
.slide-next-enter-active,
.slide-next-leave-active,
.slide-prev-enter-active,
.slide-prev-leave-active {
  transition: all 250ms cubic-bezier(0.785, 0.135, 0.15, 0.86);
}
.slide-prev-leave-to,
.slide-next-enter {
  transform: translate3d(-50%, 0, 0);
  opacity: 0;
}
.slide-prev-enter,
.slide-next-leave-to {
  transform: translate3d(50%, 0, 0);
  opacity: 0;
}
</style>
