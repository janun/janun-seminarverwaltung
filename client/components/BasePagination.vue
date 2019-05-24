<template>
  <nav
    v-if="pageCount > 1"
    class="pagination"
    @keydown.prevent.left="prev"
    @keydown.prevent.right="next"
  >
    <button class="page" :disabled="isFirst" @click="prev">
      <svg class="fill-current h-3 w-3" viewBox="0 0 20 20">
        <polygon
          points="3.828 9 9.899 2.929 8.485 1.515 0 10 .707 10.707 8.485 18.485 9.899 17.071 3.828 11 20 11 20 9 3.828 9"
        />
      </svg>
    </button>

    <template v-if="pageCount > 4">
      <button
        class="page"
        :disabled="value === 1"
        :class="value === 1 ? 'active' : 'cursor-pointer'"
        @click="onClick(1)"
      >
        1
      </button>

      <span v-if="value > 2" class="mx-1">…</span>

      <button
        v-if="value !== 1 && value !== pageCount"
        disabled
        class="page active"
      >
        {{ value }}
      </button>

      <span v-if="value < pageCount - 1">…</span>

      <button
        class="page"
        :disabled="value === pageCount"
        :class="value === pageCount ? 'active' : 'cursor-pointer'"
        @click="onClick(pageCount)"
      >
        {{ pageCount }}
      </button>
    </template>

    <template v-else>
      <button
        v-for="page in pageCount"
        :key="page"
        class="page"
        :class="value === page ? 'active' : 'cursor-pointer'"
        :disabled="value === page"
        @click="onClick(page)"
      >
        {{ page }}
      </button>
    </template>

    <button class="page" :disabled="isLast" @click="next">
      <svg class="fill-current h-3 w-3" viewBox="0 0 20 20">
        <polygon
          points="16.172 9 10.101 2.929 11.515 1.515 20 10 19.293 10.707 11.515 18.485 10.101 17.071 16.172 11 0 11 0 9"
        />
      </svg>
    </button>
  </nav>
</template>

<script>
export default {
  props: {
    value: { type: Number, default: 1 }, // currentPage
    total: { type: Number, required: true },
    perPage: { type: Number, required: true }
  },
  computed: {
    pageCount() {
      return Math.max(1, Math.ceil(this.total / this.perPage))
    },
    isFirst() {
      return this.value === 1
    },
    isLast() {
      return this.value === this.pageCount
    }
  },
  methods: {
    onClick(page) {
      this.$emit('input', page)
    },
    next() {
      if (!this.isLast) {
        this.$emit('input', this.value + 1)
      }
    },
    prev() {
      if (!this.isFirst) {
        this.$emit('input', this.value - 1)
      }
    }
  }
}
</script>

<style lang="postcss" scoped>
.pagination {
  @apply inline-flex items-center flex-wrap bg-white shadow rounded select-none h-8;
}

.page {
  @apply flex items-center justify-center px-2 mx-1 text-sm;
}

.page:disabled {
  @apply text-gray-600;
}

.active {
  @apply font-bold;
}
.active:disabled {
  @apply text-gray-700;
}
</style>
