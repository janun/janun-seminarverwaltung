<template>
  <div class="relative rounded-lg bg-white shadow-md p-5">
    <div v-if="$scopedSlots.heading" class="border-b -mx-5 px-5 pb-5 mb-8">
      <slot name="heading" v-bind="attributes" />
    </div>

    <div class="flex pb-20">
      <ul class="hidden md:block w-32 mr-12 -my-5 py-5 list-reset">
        <li v-for="(step, index) in steps" :key="index" class="flex items-center justify-start">
          <button
            :disabled="index === currentIndex"
            type="button"
            class="text-grey-darkest my-2"
            @click="goto(index)"
          >
            <span :class="{ 'font-bold': index === currentIndex }">
              {{ step.title }}
            </span>
          </button>
          <svg
            v-if="maxVisited > index && step.v.$invalid"
            class="ml-2 h-4 w-4 fill-current text-white bg-red rounded-full"
            viewBox="0 0 24 24"
          >
            <path
              d="M13.41 12l2.83 2.83a1 1 0 0 1-1.41 1.41L12 13.41l-2.83 2.83a1 1 0 1 1-1.41-1.41L10.59 12 7.76 9.17a1 1 0 0 1 1.41-1.41L12 10.59l2.83-2.83a1 1 0 0 1 1.41 1.41L13.41 12z"
            />
          </svg>
          <svg
            v-if="maxVisited > index && !step.v.$invalid"
            class="ml-2 h-4 w-4 fill-current text-white bg-green rounded-full"
            viewBox="0 0 24 24"
          >
            <path
              d="M10 14.59l6.3-6.3a1 1 0 0 1 1.4 1.42l-7 7a1 1 0 0 1-1.4 0l-3-3a1 1 0 0 1 1.4-1.42l2.3 2.3z"
            />
          </svg>
        </li>
      </ul>
      <div class="flex-auto">
        <slot />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

interface Step {
  isActive: boolean;
}

export default Vue.extend({
  provide(): object {
    return {
      nextStep: this.next,
      prevStep: this.prev,
      isFirstGetter: () => this.isFirst,
      isLastGetter: () => this.isLast
    };
  },
  data: () => ({
    currentIndex: 0,
    maxVisited: 0,
    steps: [] as Step[]
  }),
  computed: {
    isLast(): boolean {
      return this.currentIndex === this.steps.length - 1;
    },
    isFirst(): boolean {
      return this.currentIndex === 0;
    },
    currentStep(): Step {
      return this.steps[this.currentIndex];
    },
    attributes(): object {
      return {
        currentIndex: this.currentIndex,
        totalSteps: this.steps.length,
        nextStep: this.next,
        prevStep: this.prev,
        isFirst: this.isFirst,
        isLast: this.isLast,
        currentStep: this.currentStep
      };
    }
  },
  watch: {
    currentIndex: {
      handler(newStep, oldStep) {
        this.$nextTick(() => {
          if (this.steps.length === 0) {
            return;
          }
          if (oldStep !== undefined) {
            this.steps[oldStep].isActive = false;
          }
          this.steps[newStep].isActive = true;
          if (newStep >= this.maxVisited) {
            this.maxVisited = newStep;
          }
        });
      },
      immediate: true
    }
  },
  mounted() {
    this.steps = ((this.$slots.default || []).map(
      (vnode) => vnode.componentInstance
    ) as any) as Step[];
  },
  methods: {
    next() {
      if (this.isLast) {
        return;
      }
      this.currentIndex += 1;
    },
    prev() {
      if (this.isFirst) {
        return;
      }
      this.currentIndex -= 1;
    },
    goto(index: number) {
      this.currentIndex = index;
    }
  }
});
</script>
