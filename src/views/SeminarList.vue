<template>
  <div>
    <h1>Seminare</h1>
    <div class="d-flex flex-wrap align-items-center mx-n2">
      <BFormInput
        v-model="titleFilter"
        class="d-inline-block m-md-2"
        style="width: auto"
        placeholder="Filter nach Titel"
      />
      <FilterDropdown
        label="Jahr"
        v-model="yearFilter"
        :options="$store.getters['seminars/occuringYears']"
      />
      <FilterDropdown label="Quartal" v-model="quarterFilter" :options="[1, 2, 3, 4]" />
      <FilterDropdown label="Status" v-model="stateFilter" :options="possibleStates" />
      <FilterDropdown
        label="Gruppe"
        v-model="groupFilter"
        :options="$store.getters['seminars/occuringGroupNames']"
      />
      <BButton @click="resetFilters" variant="link">Reset</BButton>
    </div>

    <div class="d-flex align-items-start my-3">
      <div class="d-flex flex-column align-items-end mr-4">
        <div class="text-secondary"># Seminare</div>
        <div style="font-size:1.5rem">{{ rows | number }}</div>
      </div>

      <div class="d-flex flex-column align-items-end mx-4">
        <div class="text-secondary">Förderung</div>
        <div style="font-size:1.5rem">{{ funding_total | euro }}</div>
        <div>Min {{ Math.min(...filteredSeminars.map((s) => s.requested_funding)) | euro }}</div>
        <div>Med {{ funding_median | euro }}</div>
        <div>Ø {{ funding_average | euro }}</div>
        <div>Max {{ Math.max(...filteredSeminars.map((s) => s.requested_funding)) | euro }}</div>
      </div>

      <div class="d-flex flex-column align-items-end mx-4">
        <div class="text-secondary">TNT</div>
        <div style="font-size:1.5rem">{{ tnt_total | number }}</div>
        <div>Min {{ Math.min(...filteredSeminars.map((s) => s.tnt)) | number }}</div>
        <div>Med {{ tnt_median | number }}</div>
        <div>Ø {{ tnt_average | number }}</div>
        <div>Max {{ Math.max(...filteredSeminars.map((s) => s.tnt)) | number }}</div>
      </div>

      <div class="d-flex flex-column align-items-end mx-4">
        <div class="text-secondary">€/TNT</div>
        <div style="font-size:1.5rem">Ø {{ tnt_cost_average | euro }}</div>
        <div>Min {{ Math.min(...filteredSeminars.map((s) => s.tnt_cost)) | euro }}</div>
        <div>Med. {{ tnt_cost_median | euro }}</div>
        <div>Ø {{ tnt_cost_average | euro }}</div>
        <div>Max {{ Math.max(...filteredSeminars.map((s) => s.tnt_cost)) | euro }}</div>
      </div>

      <BPagination
        v-if="rows > perPage"
        v-model="currentPage"
        :total-rows="rows"
        :per-page="perPage"
        aria-controls="seminar-table"
        align="right"
        class="ml-auto mt-auto"
      />
    </div>

    <BTable
      id="seminar-table"
      hover
      :items="filteredSeminars"
      :busy="loading"
      :fields="fields"
      :per-page="perPage"
      :current-page="currentPage"
      sort-by="start_date"
      :sort-desc="true"
      primary-key="pk"
    >
      <div slot="table-busy" class="text-center text-danger my-2">
        <BSpinner class="align-middle mr-2"></BSpinner>
        <strong>Laden...</strong>
      </div>
      <div slot="title" slot-scope="{ value, item }">
        <b-link :to="{ name: 'SeminarDetail', params: { pk: item.pk } }">
          {{ value }}
        </b-link>
      </div>
      <div slot="group.name" slot-scope="{ value, item }">
        <b-link :to="{ name: 'GroupDetail', params: { pk: item.pk } }">
          {{ value }}
        </b-link>
      </div>
      <div slot="owner.name" slot-scope="{ value, item }">
        <b-link :to="{ name: 'UserDetail', params: { pk: item.pk } }">
          {{ value }}
        </b-link>
      </div>
    </BTable>

    <BPagination
      v-if="rows > perPage"
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="seminar-table"
      align="center"
    />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Seminar, SeminarStatus } from "@/types";
import { TableFieldArray } from "bootstrap-vue";
import FilterDropdown from "@/components/FilterDropdown.vue";

function getQuarter(date: Date): number {
  return Math.floor((date.getMonth() + 3) / 3);
}

function sum(values: number[]): number {
  return values.reduce((accumulator, value) => accumulator + value, 0);
}

function median(values: number[]): number {
  values.sort((a, b) => a - b);
  const half = Math.floor(values.length / 2);
  if (values.length % 2) {
    return values[half];
  }
  return (values[half - 1] + values[half]) / 2.0;
}

export default Vue.extend({
  components: { FilterDropdown },
  data: () => ({
    loading: true,
    perPage: 50,
    currentPage: 1,
    yearFilter: [new Date().getFullYear()] as number[],
    quarterFilter: [] as number[],
    titleFilter: "",
    groupFilter: [] as string[],
    stateFilter: [] as SeminarStatus[],
    fields: [
      {
        label: "Nr.",
        key: "pk",
        sortable: true
      },
      {
        label: "Titel",
        key: "title",
        sortable: true,
        isRowHeader: true
      },
      {
        key: "start_date",
        label: "Datum",
        sortable: true,
        formatter: (d: string): string => new Date(d).toLocaleDateString(),
        class: "text-right",
        sortDirection: "desc"
      },
      {
        key: "status",
        sortable: true
      },
      {
        key: "owner.name",
        label: "Anmelder_in",
        sortable: true
      },
      {
        key: "group.name",
        label: "Gruppe",
        sortable: true
      },
      {
        key: "planned_attendees_max",
        label: "TN",
        headerTitle: "Anzahl Teilnehmer_innen",
        formatter: "formatNumber",
        sortable: true,
        class: "text-right"
      },
      {
        key: "tnt",
        label: "TNT",
        headerTitle: "Anzahl Teilnehmer_innen-Tage",
        formatter: "formatNumber",
        sortable: true,
        class: "text-right"
      },
      {
        key: "requested_funding",
        label: "Förderung",
        sortable: true,
        formatter: "formatEuro",
        class: "text-right"
      },
      {
        key: "tnt_cost",
        label: "€/TNT",
        formatter: "formatEuro",
        sortable: true,
        class: "text-right"
      }
    ] as TableFieldArray
  }),
  async mounted() {
    this.loading = true;
    try {
      await this.$store.dispatch("seminars/fetchAll");
    } catch (e) {
      this.$store.commit("alerts/add", {
        variant: "danger",
        text: "Seminare konnten nicht geladen werden."
      });
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatNumber(value: number): string {
      return value.toLocaleString();
    },
    formatEuro(value: number): string {
      return value.toLocaleString("de-DE", {
        style: "currency",
        currency: "EUR"
      });
    },
    resetFilters() {
      this.yearFilter = [new Date().getFullYear()];
      this.quarterFilter = [];
      this.titleFilter = "";
      this.groupFilter = [];
      this.stateFilter = [];
    }
  },
  computed: {
    funding_total(): number {
      return sum(this.filteredSeminars.map((s) => s.requested_funding));
    },
    funding_average(): number {
      return this.rows ? this.funding_total / this.rows : 0;
    },
    funding_median(): number {
      return median(this.filteredSeminars.map((s) => s.requested_funding));
    },

    tnt_total(): number {
      return sum(this.filteredSeminars.map((s) => s.tnt));
    },
    tnt_average(): number {
      return this.rows ? this.tnt_total / this.rows : 0;
    },
    tnt_median(): number {
      return median(this.filteredSeminars.map((s) => s.tnt));
    },

    tnt_cost_average(): number {
      return this.tnt_total ? this.funding_total / this.tnt_total : 0;
    },
    tnt_cost_median(): number {
      return median(this.filteredSeminars.map((s) => s.tnt_cost));
    },

    possibleStates(): string[] {
      return Object.values(SeminarStatus);
    },
    filteredSeminars(): Seminar[] {
      let filtered: Seminar[] = this.$store.getters["seminars/all"];
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

      if (this.groupFilter.length > 0) {
        filtered = filtered.filter((seminar) => {
          return this.groupFilter.includes(seminar.group ? seminar.group.name : "- keine -");
        });
      }

      if (this.quarterFilter.length > 0) {
        filtered = filtered.filter((seminar) => {
          return this.quarterFilter.includes(getQuarter(new Date(seminar.start_date)));
        });
      }
      return filtered;
    },
    rows(): number {
      return this.filteredSeminars.length;
    }
  }
});
</script>
