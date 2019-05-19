<template>
  <div class="inline-flex items-stretch my-2 bg-white shadow rounded py-3">
    <div class="flex flex-col items-center mx-5">
      <span class="text-sm">Seminare</span>
      <span class="text-xl font-bold">{{ total | number }}</span>
    </div>

    <div class="flex flex-col items-center mx-5">
      <span class="text-sm">Förderung</span>
      <span class="text-xl font-bold">{{ fundingTotal | euro }}</span>
      <div class="text-sm text-center">
        <div>Ø: {{ fundingAverage | euro }}</div>
        <div>Median: {{ fundingMedian | euro }}</div>
      </div>
    </div>

    <div class="flex flex-col items-center mx-5">
      <span class="text-sm">TNT</span>
      <span class="text-xl font-bold">{{ tntTotal | number }}</span>
      <div class="text-sm text-center">
        <div>Ø: {{ tntAverage | number }}</div>
        <div>Median: {{ tntMedian | number }}</div>
      </div>
    </div>

    <div class="flex flex-col items-center mx-5">
      <span class="text-sm">Ø €/TNT</span>
      <span class="text-xl font-bold">{{ tntCostAverage | euro }}</span>
      <span class="text-sm">Median: {{ tntCostMedian | euro }}</span>
    </div>

    <div class="flex flex-col items-center mx-5">
      <span class="text-sm">Ø TN</span>
      <span class="text-xl font-bold">{{ tnAverage | number }}</span>
      <span class="text-sm">Median: {{ tnMedian | number }}</span>
    </div>

    <div class="flex flex-col items-center mx-5">
      <span class="text-sm">Ø Tage</span>
      <span class="text-xl font-bold">{{ daysAverage | number }}</span>
      <span class="text-sm">Median: {{ daysMedian | number }}</span>
    </div>
  </div>
</template>

<script>
import { sum, median } from '@/utils/math.js'

export default {
  props: {
    seminars: { type: Array, required: true }
  },
  computed: {
    total() {
      return this.seminars.length
    },
    fundingTotal() {
      return sum(this.seminars.map(s => s.requested_funding))
    },
    fundingAverage() {
      return this.total ? this.fundingTotal / this.total : 0
    },
    fundingMedian() {
      return median(this.seminars.map(s => s.requested_funding))
    },

    tntTotal() {
      return sum(this.seminars.map(s => s.tnt))
    },
    tntAverage() {
      return this.total ? this.tntTotal / this.total : 0
    },
    tntMedian() {
      return median(this.seminars.map(s => s.tnt))
    },

    tntCostAverage() {
      return this.tntTotal ? this.fundingTotal / this.tntTotal : 0
    },
    tntCostMedian() {
      return median(this.seminars.map(s => s.tnt_cost))
    },

    tnAverage() {
      const tnSum = sum(this.seminars.map(s => s.planned_attendees_max))
      return this.total ? tnSum / this.total : 0
    },
    tnMedian() {
      return median(this.seminars.map(s => s.planned_attendees_max))
    },

    daysAverage() {
      const daySum = sum(this.seminars.map(s => s.planned_training_days))
      return this.total ? daySum / this.total : 0
    },
    daysMedian() {
      return median(this.seminars.map(s => s.planned_training_days))
    }
  }
}
</script>
