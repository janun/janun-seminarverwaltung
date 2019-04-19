<template>
  <div>
    <h1 class="title">Gruppen</h1>

    <b-field grouped group-multiline>
      <b-field>
        <b-input
          ref="nameFilter"
          v-model="nameFilter"
          style="width: auto"
          placeholder="Filter nach Name"
        />
      </b-field>
    </b-field>

    <b-table :data="filteredGroups" hoverable default-sort="name" :loading="loading">
      <template slot-scope="{ row }">
        <b-table-column field="name" label="Name" sortable>
          <router-link :to="{ name: 'GroupDetail', params: { pk: row.pk } }">
            {{ row.name }}
          </router-link>
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Group } from "@/types";

export default Vue.extend({
  data: () => ({
    loading: true,
    nameFilter: ""
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
    (this.$refs.nameFilter as HTMLFormElement).focus();
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
