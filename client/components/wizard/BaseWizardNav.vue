<template>
  <ul class="list-reset">
    <li
      v-for="(step, index) in steps"
      :key="index"
      class="flex items-center justify-start"
    >
      <button
        :disabled="step.active"
        type="button"
        class="text-grey-darkest my-2"
        @click="goto(index)"
      >
        <span :class="{ 'font-bold': step.active }">
          {{ step.title }}
        </span>
      </button>

      <svg
        v-if="maxVisited > index && step.invalid"
        class="ml-2 h-4 w-4 fill-current text-white rounded-full bg-red-500"
        viewBox="0 0 24 24"
      >
        <path
          d="M13.41 12l2.83 2.83a1 1 0 0 1-1.41 1.41L12 13.41l-2.83 2.83a1 1 0 1 1-1.41-1.41L10.59 12 7.76 9.17a1 1 0 0 1 1.41-1.41L12 10.59l2.83-2.83a1 1 0 0 1 1.41 1.41L13.41 12z"
        />
      </svg>
      <svg
        v-if="step.visited && step.valid"
        class="ml-2 h-4 w-4 fill-current text-white rounded-full bg-green-500"
        viewBox="0 0 24 24"
      >
        <path
          d="M10 14.59l6.3-6.3a1 1 0 0 1 1.4 1.42l-7 7a1 1 0 0 1-1.4 0l-3-3a1 1 0 0 1 1.4-1.42l2.3 2.3z"
        />
      </svg>
    </li>
  </ul>
</template>

<script>
export default {
  inject: ['stepsGetter', 'goto', 'maxVisitedGetter'],
  computed: {
    steps() {
      return this.stepsGetter()
    },
    maxVisited() {
      return this.maxVisitedGetter()
    }
  }
}
</script>
