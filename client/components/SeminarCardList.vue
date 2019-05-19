<template>
  <div>
    <div v-if="seminars.length === 0">
      Sorry, keine Seminare gefunden.
    </div>

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
    loading: true,
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
    this.seminars = await this.$axios.$get('seminars/')
  }
}
</script>
