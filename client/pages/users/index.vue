<template>
  <div class="max-w-6xl mx-auto">
    <div class="flex flex-wrap items-center">
      <h1 class="text-green-500 text-xl font-bold">Kontos</h1>
      <nuxt-link to="/users/new" class="btn btn-outline text-green-500 ml-auto">
        Neues Konto
      </nuxt-link>
    </div>

    <div
      class="inline-flex flex-wrap items-center my-4 bg-white shadow rounded p-2"
    >
      <BaseInput
        ref="nameFilter"
        v-model="nameFilter"
        placeholder="Name oder Anmeldename"
        class="m-2"
        :class="{ 'border-green-500': nameFilter }"
      />
      <DropdownFilter
        v-model="roleFilter"
        label="Rolle"
        :options="possibleRoles"
        class="m-2"
      />
      <DropdownFilter
        v-model="groupFilter"
        label="Gruppe"
        :options="possibleGroups"
        class="m-2"
      />
      <DropdownFilter
        v-model="hatFilter"
        label="Gruppenhut"
        :options="possibleGroups"
        class="m-2"
      />

      <DropdownFilter
        v-model="reviewedFilter"
        label="überprüft"
        :options="['überprüft', 'nicht überprüft']"
        class="m-2"
      />

      <button type="button" class="m-2" @click="resetFilters">Reset</button>
    </div>

    <BaseDatatable
      :data="filteredUsers"
      :columns="columns"
      empty-message="Keine Konten gefunden."
      default-sort-field="name"
    >
      <nuxt-link
        slot="name"
        slot-scope="{ value, row }"
        class="font-bold text-gray-800"
        :to="`/users/${row.pk}`"
      >
        {{ value }}
      </nuxt-link>
    </BaseDatatable>
  </div>
</template>

<script>
import BaseDatatable from '@/components/BaseDatatable.vue'
import DropdownFilter from '@/components/DropdownFilter.vue'
import { formatDate } from '@/utils/formatters.js'

function groupNames(groups) {
  return groups.map(g => g.name).join(', ')
}

function hasIntersections(array1, array2) {
  return array1.some(value => array2.includes(value))
}

export default {
  head() {
    return {
      title: 'Alle Kontos'
    }
  },
  components: {
    BaseDatatable,
    DropdownFilter
  },
  data: () => ({
    nameFilter: '',
    roleFilter: [],
    groupFilter: [],
    hatFilter: [],
    reviewedFilter: [],
    users: [],
    groups: [],
    columns: [
      { field: 'name', label: 'Name', sortable: true },
      { field: 'username', label: 'Anmeldename', sortable: true },
      { field: 'role', label: 'Rolle', sortable: true },
      {
        field: 'janun_groups',
        label: 'Mitglied in',
        formatter: groupNames
      },
      {
        field: 'group_hats',
        label: 'Gruppenhüte',
        formatter: groupNames
      },
      {
        field: 'is_reviewed',
        label: 'überprüft',
        formatter: r => (r ? 'überprüft' : 'nicht geprüft'),
        sortable: true
      },
      {
        field: 'created_at',
        label: 'Erstellt',
        formatter: formatDate,
        sortable: true
      }
    ]
  }),
  computed: {
    possibleGroups() {
      return this.groups.map(g => g.name)
    },
    possibleRoles() {
      return ['Teamer_in', 'Prüfer_in', 'Verwalter_in']
    },
    filteredUsers() {
      let filtered = this.users
      if (this.nameFilter) {
        filtered = filtered.filter(
          user =>
            user.name.toLowerCase().indexOf(this.nameFilter.toLowerCase()) >
              -1 ||
            user.username.toLowerCase().indexOf(this.nameFilter.toLowerCase()) >
              -1
        )
      }
      if (this.groupFilter.length > 0) {
        filtered = filtered.filter(user =>
          hasIntersections(this.groupFilter, user.janun_groups.map(g => g.name))
        )
      }
      if (this.hatFilter.length > 0) {
        filtered = filtered.filter(user =>
          hasIntersections(this.hatFilter, user.group_hats.map(g => g.name))
        )
      }
      if (this.roleFilter.length > 0) {
        filtered = filtered.filter(user => this.roleFilter.includes(user.role))
      }
      if (this.reviewedFilter.length > 0) {
        const reviewedFilter = this.reviewedFilter.map(f => f === 'überprüft')
        filtered = filtered.filter(user =>
          reviewedFilter.includes(user.is_reviewed)
        )
      }
      return filtered
    }
  },
  async asyncData({ $axios }) {
    const [users, groups] = await Promise.all([
      $axios.$get('/users/'),
      $axios.$get('/group_names/')
    ])
    return { users, groups }
  },
  mounted() {
    this.$refs.nameFilter.focus()
  },
  methods: {
    resetFilters() {
      this.nameFilter = ''
      this.roleFilter = []
      this.reviewedFilter = []
    }
  }
}
</script>
