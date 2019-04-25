<template>
  <div>
    <nav class="flex items-center flex-wrap -mx-1">
      <button class="page" :class="{ 'cursor-pointer': !isFirst }" @click="prev">
        <svg class="fill-current h-3 w-3" viewBox="0 0 20 20">
          <polygon
            points="3.828 9 9.899 2.929 8.485 1.515 0 10 .707 10.707 8.485 18.485 9.899 17.071 3.828 11 20 11 20 9 3.828 9"
          />
        </svg>
      </button>

      <template v-if="pageCount > 3">
        <button class="page" :class="value === 1 ? 'active' : 'cursor-pointer'" @click="onClick(1)">
          1
        </button>
        <span class="mx-1" v-if="value > 2">…</span>
        <button class="page active" v-if="value !== 1 && value !== pageCount">
          {{ value }}
        </button>
        <span class="mx-1" v-if="value < pageCount - 1">…</span>
        <button
          class="page"
          :class="value === pageCount ? 'active' : 'cursor-pointer'"
          @click="onClick(pageCount)"
        >
          {{ pageCount }}
        </button>
      </template>

      <template v-else>
        <button
          v-for="page in pageCount"
          class="page"
          :class="value === page ? 'active' : 'cursor-pointer'"
          @click="onClick(page)"
        >
          {{ page }}
        </button>
      </template>

      <button class="page" :class="{ 'cursor-pointer': !isLast }" @click="next">
        <svg class="fill-current h-3 w-3" viewBox="0 0 20 20">
          <polygon
            points="16.172 9 10.101 2.929 11.515 1.515 20 10 19.293 10.707 11.515 18.485 10.101 17.071 16.172 11 0 11 0 9"
          />
        </svg>
      </button>
    </nav>
  </div>
</template>


<script lang="ts">
import Vue from 'vue';
export default Vue.extend({
  props: {
    value: { type: Number, default: 1 }, // currentPage
    total: { type: Number, required: true },
    perPage: { type: Number, default: 20 },
    handleArrows: { type: Boolean, default: false }
  },
  computed: {
    pageCount(): number {
      return Math.ceil(this.total / this.perPage);
    },
    isFirst(): boolean {
      return this.value === 1;
    },
    isLast(): boolean {
      return this.value === this.pageCount;
    }
  },
  methods: {
    onClick(page: number) {
      this.$emit('input', page);
    },
    next() {
      if (!this.isLast) {
        this.$emit('input', this.value + 1);
      }
    },
    prev() {
      if (!this.isFirst) {
        this.$emit('input', this.value - 1);
      }
    }
  }
});
</script>

<style lang="postcss" scoped>
.page {
  @apply flex items-center justify-center border rounded bg-white h-8 w-8 m-1 select-none;
}

.active {
  @apply text-white bg-green-400;
}
</style>
