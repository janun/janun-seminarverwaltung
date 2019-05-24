<template>
  <div class="max-w-6xl mx-auto">
    <div class="flex flex-wrap items-center">
      <h1 class="text-green-500 text-xl font-bold">Gruppen</h1>
      <nuxt-link
        class="ml-auto btn btn-outline text-green-500"
        to="/groups/new"
      >
        Neue Gruppe
      </nuxt-link>
    </div>

    <div
      class="inline-flex flex-wrap items-center my-4 bg-white shadow rounded p-2"
    >
      <BaseInput
        ref="nameFilter"
        v-model="nameFilter"
        placeholder="Filter nach Name"
        class="m-2"
        :class="{ 'border-green-500': nameFilter }"
      />
      <button type="button" class="m-2" @click="resetFilters">Reset</button>
    </div>

    <BaseDatatable
      :data="filteredGroups"
      :columns="columns"
      empty-message="Keine Gruppen gefunden."
      default-sort-field="name"
    >
      <nuxt-link
        slot="name"
        slot-scope="{ value, row }"
        class="font-bold text-gray-800"
        :to="`/groups/${row.pk}`"
      >
        {{ value }}
      </nuxt-link>
    </BaseDatatable>
  </div>
</template>

<script>
import BaseDatatable from '@/components/BaseDatatable.vue'

export default {
  components: {
    BaseDatatable
  },
  data() {
    return {
      nameFilter: '',
      columns: [{ field: 'name', label: 'Name', sortable: true }],
      groups: []
    }
  },
  computed: {
    filteredGroups() {
      let filtered = this.groups
      if (this.nameFilter) {
        filtered = filtered.filter(
          g => g.name.toLowerCase().indexOf(this.nameFilter.toLowerCase()) > -1
        )
      }
      return filtered
    }
  },
  async asyncData({ $axios }) {
    const data = await $axios.$get('/groups/')
    return { groups: data }
  },
  mounted() {
    this.$refs.nameFilter.focus()
  },
  methods: {
    resetFilters() {
      this.nameFilter = ''
    }
  }
}
</script>
