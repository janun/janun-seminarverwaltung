<template>
  <div class="mx-auto xl:px-4" style="max-width:100rem">
    <div v-if="loading" class="fullspinner" />

    <h1 class="text-green-500 text-2xl font-bold mb-5">Seminare</h1>

    <div class="flex flex-wrap items-center -mx-2 my-4">
      <BaseInput
        ref="titleFitler"
        v-model="titleFilter"
        placeholder="Filter nach Titel"
        class="m-2"
        :class="{ 'border-green-500': titleFilter }"
      />
      <DropdownFilter v-model="quarterFilter" label="Quartal" :options="[1, 2, 3, 4]" class="m-2" />
      <DropdownFilter
        v-model="yearFilter"
        label="Jahr"
        :options="$store.getters['seminars/occuringYears']"
        class="m-2"
      />
      <DropdownFilter v-model="stateFilter" label="Status" :options="allStates" class="m-2" />
      <DropdownFilter
        v-model="groupFilter"
        label="Gruppe"
        :options="$store.getters['seminars/occuringGroupNames']"
        class="m-2"
      />
      <BaseCheckbox
        v-model="deadlineFilter"
        title="Deadline abgelaufen"
        class="mx-2 px-4 bg-white py-2 shadow rounded border flex items-center"
      >
        Deadline
      </BaseCheckbox>

      <button type="button" class="m-2" @click="resetFilters">Reset</button>
    </div>

    <SeminarStats :seminars="filteredSeminars" />

    <BaseDatatable
      class="my-4"
      :per-page="100"
      :data="filteredSeminars"
      :columns="columns"
      :loading="loading"
      :empty-message="loading ? 'Laden…' : 'Keine Seminare gefunden.'"
      default-sort-field="start_date"
      :default-sort-dir="-1"
      @sortChanged="currentPage = 1"
    >
      <router-link
        slot="title"
        slot-scope="{ value, row }"
        class="font-bold text-gray-800"
        :to="{ name: 'SeminarDetail', params: { pk: row.pk } }"
      >
        {{ value }}
      </router-link>
      <router-link
        slot="owner"
        slot-scope="{ value }"
        :to="{ name: 'UserDetail', params: { pk: value.pk } }"
      >
        {{ value.name }}
      </router-link>
      <template slot="group" slot-scope="{ value }">
        <router-link v-if="value" :to="{ name: 'GroupDetail', params: { pk: value.pk } }">
          {{ value.name }}
        </router-link>
      </template>
      <template slot="status" slot-scope="{ value }">
        <StatusBadge :value="value" />
      </template>
    </BaseDatatable>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { Seminar, User, Group } from '@/types';
import BaseDatatable from '@/components/BaseDatatable.vue';
import BaseInput from '@/components/BaseInput.vue';
import DropdownFilter from '@/components/DropdownFilter.vue';
import BaseCheckbox from '@/components/BaseCheckbox.vue';
import StatusBadge from '@/components/StatusBadge.vue';
import SeminarStats from '@/components/SeminarStats.vue';

import { Column } from '@/components/BaseDatatable.vue';
import { formatDate, formatEuro } from '@/utils/formatters.ts';
import { getQuarter } from '@/utils/date.ts';
import { states, getStateInfo } from '../utils/status';

export default Vue.extend({
  components: {
    BaseDatatable,
    DropdownFilter,
    BaseInput,
    BaseCheckbox,
    StatusBadge,
    SeminarStats
  },
  data: () => ({
    perPage: 100,
    currentPage: 1,
    loading: true,
    yearFilter: [new Date().getFullYear()] as number[],
    quarterFilter: [] as number[],
    titleFilter: '',
    groupFilter: [] as string[],
    stateFilter: [] as string[],
    deadlineFilter: false,
    columns: [
      { field: 'title', label: 'Titel', sortable: true, width: '30rem' },
      { field: 'start_date', label: 'Datum', sortable: true, formatter: formatDate },
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
      { field: 'tnt', label: 'TNT', sortable: true, tooltip: 'Teilnehmenden-Tage' },
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
    ] as Column[]
  }),
  computed: {
    allStates(): string[] {
      return states;
    },
    filteredSeminars(): Seminar[] {
      let filtered: Seminar[] = this.$store.getters['seminars/all'];
      if (this.titleFilter) {
        filtered = filtered.filter(
          (seminar) => seminar.title.toLowerCase().indexOf(this.titleFilter.toLowerCase()) > -1
        );
      }
      if (this.yearFilter.length > 0) {
        filtered = filtered.filter((seminar) =>
          this.yearFilter.includes(new Date(seminar.start_date).getFullYear())
        );
      }
      if (this.stateFilter.length > 0) {
        filtered = filtered.filter((seminar) => this.stateFilter.includes(seminar.status));
      }
      if (this.deadlineFilter) {
        filtered = filtered.filter((seminar) => new Date(seminar.deadline) < new Date());
      }
      if (this.groupFilter.length > 0) {
        filtered = filtered.filter((seminar) => {
          return this.groupFilter.includes(seminar.group ? seminar.group.name : '- keine -');
        });
      }
      if (this.quarterFilter.length > 0) {
        filtered = filtered.filter((seminar) => {
          return this.quarterFilter.includes(getQuarter(new Date(seminar.start_date)));
        });
      }
      return filtered;
    }
  },
  watch: {
    filteredSeminars() {
      this.currentPage = 1;
    }
  },
  async mounted() {
    this.loading = true;
    try {
      await this.$store.dispatch('seminars/fetchAll');
    } catch (e) {
      alert('Seminare konnten nicht geladen werden.');
    } finally {
      this.loading = false;
    }
    (this.$refs.titleFitler as HTMLInputElement).focus();
  },
  methods: {
    resetFilters() {
      this.yearFilter = [new Date().getFullYear()];
      this.quarterFilter = [];
      this.titleFilter = '';
      this.groupFilter = [];
      this.stateFilter = [];
      this.deadlineFilter = false;
    }
  }
});
</script>
