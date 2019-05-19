<template>
  <div>
    <h1 class="text-green-500 font-bold text-xl mb-2">Seminare</h1>

    <SeminarStats :seminars="filteredSeminars" class="my-2" />

    <div class="flex flex-wrap items-end my-4">
      <div class="flex flex-wrap bg-white shadow rounded p-2">
        <BaseInput
          ref="titleFilter"
          v-model="titleFilter"
          placeholder="Filter nach Titel"
          class="m-2"
          :class="{ 'border-green-500': titleFilter }"
        />
        <DropdownFilter
          v-model="quarterFilter"
          label="Quartal"
          :options="[1, 2, 3, 4]"
          class="m-2"
        />
        <DropdownFilter
          v-model="yearFilter"
          label="Jahr"
          :options="allYears"
          class="m-2"
        />
        <DropdownFilter
          v-model="stateFilter"
          label="Status"
          :options="allStates"
          class="m-2"
        />
        <DropdownFilter
          v-model="groupFilter"
          label="Gruppe"
          :options="allGroups"
          class="m-2"
        />
        <BaseCheckbox
          v-model="deadlineFilter"
          title="Deadline abgelaufen"
          class="m-2 p-2 flex items-center"
        >
          Deadline
        </BaseCheckbox>

        <button type="button" class="mx-4 my-4" @click="resetFilters">
          Reset
        </button>
      </div>

      <BasePagination
        v-model="currentPage"
        :total="filteredSeminars.length"
        :per-page="50"
        class="ml-auto mr-2"
      />
    </div>

    <BaseDatatable
      :per-page="50"
      :current-page="currentPage"
      :data="filteredSeminars"
      :columns="columns"
      default-sort-field="start_date"
      :default-sort-dir="-1"
    >
      <nuxt-link
        slot="title"
        slot-scope="{ value, row }"
        class="font-bold text-gray-800"
        :to="`/seminars/${row.pk}`"
      >
        {{ value }}
      </nuxt-link>
      <nuxt-link
        v-if="value"
        slot="owner"
        slot-scope="{ value }"
        :to="`/users/${value.pk}`"
      >
        {{ value.name }}
      </nuxt-link>
      <template slot="group" slot-scope="{ value }">
        <nuxt-link v-if="value" :to="`/groups/${value.pk}`">
          {{ value.name }}
        </nuxt-link>
      </template>
      <template slot="status" slot-scope="{ value }">
        <StatusBadge :value="value" />
      </template>
    </BaseDatatable>

    <div class="flex items-center my-4">
      <BasePagination
        v-model="currentPage"
        :total="filteredSeminars.length"
        :per-page="50"
        class="ml-auto"
      />
    </div>
  </div>
</template>

<script>
import BaseDatatable from '@/components/BaseDatatable.vue'
import BasePagination from '@/components/BasePagination.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import SeminarStats from '@/components/SeminarStats.vue'
import { formatDate, formatEuro } from '@/utils/formatters.js'
import DropdownFilter from '@/components/DropdownFilter.vue'
import { getQuarter } from '@/utils/date.js'
import { states } from '@/utils/status.js'

function range(start, stop, step = 1) {
  const a = [start]
  let b = start
  while (b < stop) {
    a.push((b += step))
  }
  return a
}

export default {
  components: {
    BaseDatatable,
    BasePagination,
    StatusBadge,
    DropdownFilter,
    SeminarStats
  },
  data() {
    return {
      yearFilter: [new Date().getFullYear()],
      quarterFilter: [],
      titleFilter: '',
      groupFilter: [],
      stateFilter: [],
      deadlineFilter: false,
      currentPage: 1,
      seminars: [],
      groups: [],
      columns: [
        { field: 'title', label: 'Titel', sortable: true },
        {
          field: 'start_date',
          label: 'Datum',
          sortable: true,
          formatter: formatDate
        },
        {
          field: 'status',
          label: 'Status',
          sortable: true
        },
        { field: 'owner', label: 'Besitzer' },
        { field: 'group', label: 'Gruppe' },
        {
          field: 'planned_training_days',
          label: 'B-Tage',
          sortable: true,
          tooltip: 'Bildungstage'
        },
        {
          field: 'planned_attendees_max',
          label: 'TN',
          sortable: true,
          tooltip: 'Anzahl Teilnehmende'
        },
        {
          field: 'tnt',
          label: 'TNT',
          sortable: true,
          tooltip: 'Teilnehmenden-Tage'
        },
        {
          field: 'requested_funding',
          label: 'Förderung',
          sortable: true,
          formatter: formatEuro
        },
        {
          field: 'tnt_cost',
          label: '€/TNT',
          sortable: true,
          formatter: formatEuro,
          tooltip: 'Kosten pro Teilnehmenden-Tag'
        },
        {
          field: 'deadline',
          label: 'Deadline',
          sortable: true,
          formatter: formatDate,
          tooltip: 'Deadline zum Einreichen der Abrechnung'
        },
        {
          field: 'created_at',
          label: 'Erstellt',
          sortable: true,
          formatter: formatDate,
          tooltip: 'Datum der Erstellung des DB-Eintrags'
        }
      ]
    }
  },
  computed: {
    allStates() {
      return states
    },
    allYears() {
      return range(2013, new Date().getFullYear() + 1)
    },
    allGroups() {
      return this.groups.map(g => g.name)
    },
    filteredSeminars() {
      let filtered = this.seminars
      if (this.titleFilter) {
        filtered = filtered.filter(
          seminar =>
            seminar.title
              .toLowerCase()
              .indexOf(this.titleFilter.toLowerCase()) > -1
        )
      }
      if (this.yearFilter.length > 0) {
        filtered = filtered.filter(seminar =>
          this.yearFilter.includes(new Date(seminar.start_date).getFullYear())
        )
      }
      if (this.stateFilter.length > 0) {
        filtered = filtered.filter(seminar =>
          this.stateFilter.includes(seminar.status)
        )
      }
      if (this.deadlineFilter) {
        filtered = filtered.filter(
          seminar => new Date(seminar.deadline) < new Date()
        )
      }
      if (this.groupFilter.length > 0) {
        filtered = filtered.filter(seminar => {
          return this.groupFilter.includes(
            seminar.group ? seminar.group.name : '- keine -'
          )
        })
      }
      if (this.quarterFilter.length > 0) {
        filtered = filtered.filter(seminar => {
          return this.quarterFilter.includes(
            getQuarter(new Date(seminar.start_date))
          )
        })
      }
      return filtered
    }
  },
  watch: {
    async yearFilter(newYear, oldYear) {
      this.seminars = await this.$axios.$get('/seminars/', {
        params: { year: newYear }
      })
    },
    filteredSeminars() {
      this.currentPage = 1
    }
  },
  async asyncData({ $axios }) {
    const [seminars, groups] = await Promise.all([
      $axios.$get('/seminars/', {
        params: { year: new Date().getFullYear() }
      }),
      $axios.$get('/group_names/')
    ])
    return { seminars, groups }
  },
  mounted() {
    this.$refs.titleFilter.focus()
  },
  methods: {
    resetFilters() {
      this.yearFilter = [new Date().getFullYear()]
      this.quarterFilter = []
      this.titleFilter = ''
      this.groupFilter = []
      this.stateFilter = []
      this.deadlineFilter = false
    }
  }
}
</script>
