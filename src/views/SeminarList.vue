<template>
  <div>
    <h1 class="title has-text-primary">Seminare</h1>

    <b-field grouped group-multiline>
      <b-field>
        <b-input
          ref="titleFilter"
          v-model="titleFilter"
          style="width: auto"
          placeholder="Filter nach Titel"
        />
      </b-field>
      <b-field>
        <FilterDropdown
          label="Jahr"
          v-model="yearFilter"
          :options="$store.getters['seminars/occuringYears']"
        />
      </b-field>
      <b-field>
        <FilterDropdown label="Quartal" v-model="quarterFilter" :options="[1, 2, 3, 4]" />
      </b-field>
      <b-field>
        <FilterDropdown label="Status" v-model="stateFilter" :options="possibleStates" />
      </b-field>
      <b-field>
        <FilterDropdown
          label="Gruppe"
          v-model="groupFilter"
          :options="$store.getters['seminars/occuringGroupNames']"
        />
      </b-field>
      <b-field> <BButton @click="resetFilters" type="is-light">Reset</BButton></b-field>
    </b-field>

    <!-- <div class="level">
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
    </div> -->

    <b-table
      :data="filteredSeminars"
      hoverable
      paginated
      :per-page="perPage"
      default-sort="start_date"
      default-sort-direction="desc"
      :loading="loading"
    >
      <template slot-scope="{ row }">
        <b-table-column field="title" label="Titel" sortable>
          <router-link :to="{ name: 'SeminarDetail', params: { pk: row.pk } }">
            {{ row.title }}
          </router-link>
        </b-table-column>
        <b-table-column field="start_date" label="Datum" sortable numeric>
          {{ row.start_date | date }}
        </b-table-column>
        <b-table-column field="status" label="Status" sortable>
          {{ row.status }}
        </b-table-column>
        <b-table-column field="owner.name" label="Besitzer" sortable>
          {{ row.owner.name }}
        </b-table-column>
        <b-table-column field="group.name" label="Gruppe" sortable>
          {{ row.group ? row.group.name : "" }}
        </b-table-column>
        <b-table-column field="planned_attendees_max" label="TN" sortable numeric>
          {{ row.planned_attendees_max }}
        </b-table-column>
        <b-table-column field="tnt" label="TNT" sortable numeric>
          {{ row.tnt }}
        </b-table-column>
        <b-table-column field="requested_funding" label="Förderung" sortable numeric>
          {{ row.requested_funding }}
        </b-table-column>
        <b-table-column field="tnt_cost" label="€/TNT" sortable numeric>
          {{ row.tnt_cost }}
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Seminar, SeminarStatus } from "@/types";
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
    perPage: 25,
    currentPage: 1,
    yearFilter: [new Date().getFullYear()] as number[],
    quarterFilter: [] as number[],
    titleFilter: "",
    groupFilter: [] as string[],
    stateFilter: [] as SeminarStatus[],
    columns: [
      { field: "title", label: "Titel", sortable: true },
      { field: "start_date", label: "Datum", sortable: true },
      { field: "status", label: "Status", sortable: true },
      { field: "owner.name", label: "Besitzer", sortable: true },
      // { field: "group ? group.name: ''", label: "Gruppe", sortable: true },
      { field: "planned_attendees_max", label: "TN", sortable: true },
      { field: "tnt", label: "TNT", sortable: true },
      { field: "requested_funding", label: "Förderung", sortable: true },
      { field: "tnt_cost", label: "€/TNT", sortable: true }
    ]
  }),
  async mounted() {
    this.loading = true;
    try {
      await this.$store.dispatch("seminars/fetchAll");
    } catch (e) {
      alert("Seminare konnten nicht geladen werden.");
    } finally {
      this.loading = false;
    }
    (this.$refs.titleFilter as HTMLFormElement).focus();
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
