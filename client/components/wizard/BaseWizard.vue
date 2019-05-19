<template>
  <div>
    <slot />
  </div>
</template>

<script>
export default {
  props: {
    title: { type: String, default: '' }
  },
  data: () => ({
    currentIndex: 0,
    maxVisited: 0,
    steps: []
  }),
  provide() {
    return {
      stepsGetter: () => this.steps,
      goto: this.goto,
      currentIndexGetter: () => this.currentIndex,
      maxVisitedGetter: () => this.maxVisited,
      next: this.next,
      prev: this.prev,
      wizardTitle: this.title
    }
  },
  watch: {
    currentIndex: {
      handler(newIndex, oldIndex) {
        this.$nextTick(() => {
          if (oldIndex != null) {
            this.steps[oldIndex].active = false
          }
          this.steps[newIndex].active = true
          if (newIndex > this.maxVisited) {
            this.maxVisited = newIndex
          }
        })
      },
      immediate: true
    }
  },
  mounted() {
    if (this.$slots.default) {
      this.steps = this.$slots.default
        .map(vnode => vnode.componentInstance)
        .filter(s => s != null)
    }
  },
  methods: {
    next() {
      if (this.currentIndex !== this.steps.length - 1) {
        this.currentIndex += 1
      }
    },
    prev() {
      if (this.currentIndex !== 0) {
        this.currentIndex -= 1
      }
    },
    goto(index) {
      this.currentIndex = index
    }
  }
}
</script>
