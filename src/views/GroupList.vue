<template>
  <div>
    <div>
      <h1>Gruppen</h1>
      <BFormInput
        v-model="nameFilter"
        class="d-inline-block"
        style="width: auto"
        placeholder="Filter nach Name"
      />
    </div>

    <div class="mt-2">
      <div class="d-flex my-3">
        <span> {{ rows }} Gruppen gefunden </span>
      </div>

      <BTable
        id="group-table"
        hover
        :items="filteredGroups"
        :busy="loading"
        :fields="fields"
        primary-key="pk"
      >
        <div slot="table-busy" class="text-center text-danger my-2">
          <BSpinner class="align-middle mr-2"></BSpinner>
          <strong>Laden...</strong>
        </div>
        <div slot="name" slot-scope="{ value, item }">
          <b-link :to="{ name: 'GroupDetail', params: { id: item.pk } }">
            {{ value }}
          </b-link>
        </div>
      </BTable>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { TableFieldArray } from "bootstrap-vue";

import { Group } from "@/types";

export default Vue.extend({
  data: () => ({
    loading: true,
    nameFilter: "",
    fields: [
      {
        label: "Nr.",
        key: "pk",
        sortable: true
      },
      {
        label: "Name",
        key: "name",
        sortable: true,
        isRowHeader: true
      }
    ] as TableFieldArray
  }),
  async mounted() {
    this.loading = true;
    try {
      await this.$store.dispatch("groups/fetchAll");
    } catch (e) {
      this.$store.commit("alerts/add", {
        variant: "danger",
        text: "Gruppen konnten nicht geladen werden."
      });
    } finally {
      this.loading = false;
    }
  },
  computed: {
    filteredGroups(): Group[] {
      let filtered: Group[] = this.$store.getters["groups/all"];
      if (this.nameFilter) {
        filtered = filtered.filter(
          (group) => group.name.toLowerCase().indexOf(this.nameFilter.toLowerCase()) > -1
        );
      }
      return filtered;
    },
    rows(): number {
      return this.filteredGroups.length;
    }
  }
});
</script>
