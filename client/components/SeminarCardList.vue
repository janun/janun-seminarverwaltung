<template>
  <div>
    <div class="flex flex-wrap items-center mt-10">
      <h2 class="text-gray-800 font-bold text-xl">
        Deine Seminare
        <span
          v-if="seminars.length"
          class="ml-2 text-xs text-gray-600 font-normal"
        >
          {{ count }} insg.
        </span>
      </h2>
      <nuxt-link class="ml-auto btn btn-primary" to="/seminars/apply">
        Seminar anmelden
      </nuxt-link>
    </div>

    <div v-if="seminars.length === 0 && !loading">
      Sorry, keine Seminare gefunden.
    </div>

    <div v-if="loading">Lade Seminare…</div>

    <div
      v-for="[year, seminarsInYear] in seminarsGroupedByYear"
      :key="year"
      class="mb-10"
    >
      <h4 class="text-green-500">
        {{ year }}
        <span class="text-gray-600 text-xs ml-2">
          {{ seminarsInYear.length }} Seminare
        </span>
      </h4>
      <hr class="bg-gray-300 h-px mb-5" />

      <div class="flex flex-wrap -m-4">
        <div
          v-for="seminar in seminarsInYear"
          :key="seminar.pk"
          class="lg:w-1/3 sm:w-1/2 w-full p-4"
        >
          <SeminarCard :seminar="seminar" />
        </div>
      </div>
    </div>
    <button
      v-if="next"
      class="btn btn-outline text-gray-700 mx-auto my-2"
      :class="{ 'btn-loading': loadingMore }"
      @click="loadMore"
    >
      Mehr laden
    </button>
  </div>
</template>

<script>
import SeminarCard from '@/components/SeminarCard.vue'

function groupBy(list, keyGetter) {
  const map = new Map()
  list.forEach(item => {
    const key = keyGetter(item)
    const collection = map.get(key)
    if (!collection) {
      map.set(key, [item])
    } else {
      collection.push(item)
    }
  })
  return map
}

export default {
  components: {
    SeminarCard
  },
  data: () => ({
    loading: false,
    loadingMore: false,
    count: null,
    next: '',
    seminars: []
  }),
  computed: {
    seminarsGroupedByYear() {
      return groupBy(this.seminars, seminar =>
        new Date(seminar.start_date).getFullYear()
      )
    }
  },
  async mounted() {
    console.log('DEBUG')
    this.loading = true
    try {
      const data = await this.$axios.$get('seminars/', {
        params: { owner: this.$auth.user.pk, limit: 50 }
      })
      this.seminars = data.results
      this.count = data.count
      this.next = data.next
    } finally {
      this.loading = false
    }
  },
  methods: {
    async loadMore() {
      this.loadingMore = true
      try {
        const data = await this.$axios.$get(this.next)
        this.seminars.push(...data.results)
        this.count = data.count
        this.next = data.next
      } finally {
        this.loadingMore = false
      }
    }
  }
}
</script>
