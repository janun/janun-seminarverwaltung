<template>
  <div class="mx-auto xl:px-4" style="max-width:100rem">
    <div class="fullspinner" v-if="loading" />

    <h1 class="text-green-500 text-2xl font-bold mb-5">Benutzer_innen</h1>

    <div class="flex flex-wrap items-center -mx-2 my-4">
      <BaseInput
        ref="nameFitler"
        v-model="nameFilter"
        placeholder="Filter nach Name"
        class="m-2"
        :class="{ 'border-green-500': nameFilter }"
      />
      <DropdownFilter v-model="roleFilter" label="Rolle" :options="possibleRoles" class="m-2" />
      <DropdownFilter v-model="groupFilter" label="Gruppe" :options="possibleGroups" class="m-2" />
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

      <button type="button" @click="resetFilters" class="m-2">Reset</button>
    </div>

    <BaseDatatable
      class="my-4"
      :data="filteredUsers"
      :columns="columns"
      :loading="loading"
      :emptyMessage="loading ? 'Laden…' : 'Keine Benutzer_innen gefunden.'"
      defaultSortField="name"
    >
    </BaseDatatable>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { Seminar, User, Group, UserRole } from '@/types';
import BaseDatatable from '@/components/BaseDatatable.vue';
import BaseInput from '@/components/BaseInput.vue';
import DropdownFilter from '@/components/DropdownFilter.vue';
import StatusBadge from '@/components/StatusBadge.vue';
import SeminarStats from '@/components/SeminarStats.vue';

import { Column } from '@/components/BaseDatatable.vue';
import { formatDate, formatEuro } from '@/utils/formatters.ts';
import { getQuarter } from '@/utils/date.ts';
import { states, getStateInfo } from '../utils/status';

function groupNames(groups: Group[]): string {
  return groups.map((g) => g.name).join(', ');
}

function intersections<T>(array1: T[], array2: T[]): T[] {
  return array1.filter((value) => array2.includes(value));
}

function hasIntersections<T>(array1: T[], array2: T[]): boolean {
  return intersections<T>(array1, array2).length > 0;
}

export default Vue.extend({
  components: {
    BaseDatatable,
    DropdownFilter,
    BaseInput
  },
  data: () => ({
    loading: true,
    nameFilter: '',
    roleFilter: [] as string[],
    groupFilter: [] as string[],
    hatFilter: [] as string[],
    reviewedFilter: [] as string[],
    columns: [
      { field: 'name', label: 'Name', sortable: true },
      { field: 'username', label: 'Benutzername', sortable: true },
      { field: 'role', label: 'Rolle', sortable: true },
      {
        field: 'janun_groups',
        label: 'Gruppen',
        formatter: groupNames,
        tooltip: 'Mitgliedschaften in JANUN-Gruppen'
      },
      {
        field: 'group_hats',
        label: 'Gruuppenhüte',
        formatter: groupNames,
        tooltip: 'Prüf-Hüte für JANUN-Gruppen'
      },
      {
        field: 'is_reviewed',
        label: 'überprüft',
        formatter: (r) => (r ? 'Ja' : 'Nein'),
        sortable: true
      },
      {
        field: 'created_at',
        label: 'Erstellt',
        formatter: formatDate,
        tooltip: 'DB-Eintrag erstellt am',
        sortable: true
      }
    ] as Column[]
  }),
  async created() {
    this.loading = true;
    this.$store.dispatch('groups/fetchAll');
    try {
      await this.$store.dispatch('users/fetchAll');
    } catch (e) {
      alert('Benutzer_innen konnten nicht geladen werden.');
    } finally {
      this.loading = false;
    }
    (this.$refs.nameFitler as HTMLInputElement).focus();
  },
  methods: {
    resetFilters() {
      this.nameFilter = '';
      this.roleFilter = [];
      this.reviewedFilter = [];
    }
  },
  computed: {
    possibleGroups(): string[] {
      return this.$store.getters['groups/all'].map((g: Group) => g.name);
    },
    possibleRoles(): string[] {
      return Object.keys(UserRole);
    },
    filteredUsers(): User[] {
      let filtered: User[] = this.$store.getters['users/all'];
      if (this.nameFilter) {
        filtered = filtered.filter(
          (user) => user.name.toLowerCase().indexOf(this.nameFilter.toLowerCase()) > -1
        );
      }
      if (this.groupFilter.length > 0) {
        filtered = filtered.filter((user) =>
          hasIntersections(this.groupFilter, user.janun_groups.map((g) => g.name))
        );
      }
      if (this.hatFilter.length > 0) {
        filtered = filtered.filter((user) =>
          hasIntersections(this.hatFilter, user.group_hats.map((g) => g.name))
        );
      }
      if (this.roleFilter.length > 0) {
        filtered = filtered.filter((user) => this.roleFilter.includes(user.role));
      }
      if (this.reviewedFilter.length > 0) {
        const reviewedFilter: boolean[] = this.reviewedFilter.map((f) =>
          f === 'überprüft' ? true : false
        );
        filtered = filtered.filter((user) => reviewedFilter.includes(user.is_reviewed));
      }
      return filtered;
    }
  }
});
</script>
