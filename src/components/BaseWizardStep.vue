<template>
  <div v-if="active" ref="div">
    <form @submit.prevent="submit">
      <slot />

      <div
        class="absolute inset-x-0 bottom-0 flex flex-row-reverse justify-between bg-gray-100 mt-5 p-5 rounded-b-lg"
      >
        <slot name="footer" v-bind="{ isLast, isFirst }">
          <button class="btn primary flex items-center" type="submit" :disabled="invalid">
            {{ nextLabel }}
            <svg class="ml-2 fill-current h-3 w-3" viewBox="0 0 20 20">
              <path
                d="M16.172 9l-6.071-6.071 1.414-1.414L20 10l-.707.707-7.778 7.778-1.414-1.414L16.172 11H0V9z"
              />
            </svg>
          </button>
          <button type="button" class="btn tertiary flex items-center" @click="onPrev">
            <svg class="mr-2 fill-current h-3 w-3" viewBox="0 0 20 20">
              <path
                d="M3.828 9l6.071-6.071-1.414-1.414L0 10l.707.707 7.778 7.778 1.414-1.414L3.828 11H20V9H3.828z"
              />
            </svg>
            {{ prevLabel }}
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
  props: {
    title: { type: String, required: true },
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
    active: false,
    visited: false
  }),
  computed: {
    isFirst(): boolean {
      return (this.$parent as any).isFirst;
    },
    isLast(): boolean {
      return (this.$parent as any).isLast;
    },
    valid(): boolean {
      return !this.v || !this.v.$invalid;
    },
    invalid(): boolean {
      return this.v && this.v.$invalid;
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
      (this.$parent as any).next();
    },
    onPrev() {
      this.$emit('prev');
      (this.$parent as any).prev();
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
