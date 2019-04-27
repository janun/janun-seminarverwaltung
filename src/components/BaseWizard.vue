<template>
  <div class="relative rounded-lg bg-white shadow-md p-5">
    <div v-if="$scopedSlots.heading" class="border-b -mx-5 px-5 pb-5 mb-8">
      <slot name="heading" v-bind="{ currentIndex, totalSteps }" />
    </div>

    <div class="flex pb-20">
      <BaseWizardNav />
      <div class="flex-auto">
        <slot />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseWizardNav from '@/components/BaseWizardNav.vue';

interface Step {
  active: boolean;
}

export default Vue.extend({
  components: {
    BaseWizardNav
  },
  data: () => ({
    currentIndex: 0,
    maxVisited: 0,
    steps: [] as Step[]
  }),
  computed: {
    isLast(): boolean {
      return this.currentIndex === this.totalSteps - 1;
    },
    isFirst(): boolean {
      return this.currentIndex === 0;
    },
    currentStep(): Step {
      return this.steps[this.currentIndex];
    },
    totalSteps(): number {
      return this.steps.length;
    }
  },
  watch: {
    currentIndex: {
      handler(newIndex, oldIndex) {
        this.$nextTick(() => {
          if (oldIndex != null) {
            this.steps[oldIndex].active = false;
          }
          this.steps[newIndex].active = true;
          if (newIndex > this.maxVisited) {
            this.maxVisited = newIndex;
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
      if (!this.isLast) {
        this.currentIndex += 1;
      }
    },
    prev() {
      if (!this.isFirst) {
        this.currentIndex -= 1;
      }
    },
    goto(index: number) {
      this.currentIndex = index;
    }
  }
});
</script>
