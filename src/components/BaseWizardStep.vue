<template>
  <div v-if="isActive" ref="div">
    <form @submit.prevent="submit">
      <slot />

      <div
        class="absolute pin-x pin-b flex flex-row-reverse justify-between bg-grey-lighter mt-5 p-5 rounded-b-lg"
      >
        <slot name="footer" v-bind="{ next, prev, isLast, isFirst }">
          <button class="btn bg-green" type="submit" :disabled="invalid || isLast">
            Weiter
          </button>
          <button type="button" :disabled="isFirst" @click="prev">
            Zurück
          </button>
        </slot>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { Validation } from 'vuelidate';
import { getFocusableChildren } from '@/utils/utils.ts';

export default Vue.extend({
  inject: ['next', 'prev', 'isFirstGetter', 'isLastGetter'],
  props: {
    title: { type: String, required: true },
    v: { type: Object as () => Validation, default: null }
  },
  data: () => ({
    isActive: false
  }),
  computed: {
    isFirstStep(): boolean {
      return (this as any).isFirstGetter();
    },
    isLastStep(): boolean {
      return (this as any).isLastGetter();
    },
    valid(): boolean {
      return !this.v || !this.v.$invalid;
    },
    invalid(): boolean {
      return this.v && this.v.$invalid;
    }
  },
  watch: {
    isActive: {
      immediate: true,
      handler(active: boolean) {
        if (active) {
          this.focus();
        }
      }
    }
  },
  methods: {
    submit(): void {
      this.$emit('submit');
      (this as any).next();
    },
    focus(): void {
      this.$nextTick(() => {
        const focusEls = getFocusableChildren(this.$el);
        if (focusEls) {
          focusEls[0].focus();
        }
      });
    }
  }
});
</script>
