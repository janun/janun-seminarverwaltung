<template>
  <transition name="slide-next" mode="out-in">
    <div
      v-if="active"
      :key="title"
      class="absolute z-10 w-full max-w-3xl rounded-lg bg-white shadow-md p-5"
    >
      <h1 class="text-xl font-bold text-green-500 border-b -mx-5 px-5 pb-5 mb-8">
        {{ wizardTitle }}
        <span class="text-gray-700 text-sm">({{ currentIndex + 1 }}/{{ steps.length }})</span>
      </h1>

      <form @submit.prevent="submit">
        <div class="flex">
          <BaseWizardNav class="hidden md:block w-32 mr-12" />
          <div ref="content"><slot /></div>
        </div>

        <BaseWizardFooter
          class="-mx-5 -mb-5"
          :prev-label="prevLabel"
          :next-label="nextLabel"
          :invalid="invalid"
          @prev="onPrev"
        />
      </form>
    </div>
  </transition>
</template>

<script lang="ts">
import Vue from 'vue';
import { Validation } from 'vuelidate';
import { getFocusableChildren } from '@/utils/utils.ts';
import BaseWizardNav from '@/components/BaseWizardNav.vue';
import BaseWizardFooter from '@/components/BaseWizardFooter.vue';

export default Vue.extend({
  inject: ['next', 'prev', 'currentIndexGetter', 'stepsGetter', 'wizardTitle'],
  components: {
    BaseWizardNav,
    BaseWizardFooter
  },
  props: {
    title: { type: String, required: true }, // used by BaseWizardNav
    v: { type: Object as () => Validation, default: null },
    nextLabel: { type: String, default: 'Weiter' },
    prevLabel: { type: String, default: 'Zurück' }
  },
  provide() {
    return {
      formValidator: this.v
    };
  },
  data: () => ({
    active: false, // set by parent
    visited: false
  }),
  computed: {
    valid(): boolean {
      return !this.v || !this.v.$invalid;
    },
    invalid(): boolean {
      return this.v && this.v.$invalid;
    },
    currentIndex(): number {
      return (this as any).currentIndexGetter();
    },
    steps(): object[] {
      return (this as any).stepsGetter();
    }
  },
  watch: {
    active: {
      immediate: true,
      handler(active: boolean) {
        if (active) {
          this.visited = true;
          this.focus();
        }
      }
    }
  },
  methods: {
    submit() {
      this.$emit('submit');
      (this as any).next();
    },
    onPrev() {
      this.$emit('prev');
      (this as any).prev();
    },
    focus(): void {
      this.$nextTick(() => {
        const focusEls = getFocusableChildren(this.$refs.content as Element);
        if (focusEls.length) {
          focusEls[0].focus();
        }
      });
    }
  }
});
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
