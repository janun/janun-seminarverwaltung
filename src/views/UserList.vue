<template>
  <div>
    <div>
      <h1>Benutzer_innen</h1>
      <BFormInput
        v-model="nameFilter"
        class="d-inline-block"
        style="width: auto"
        placeholder="Filter nach Name"
      />
    </div>

    <div class="mt-2">
      <div class="d-flex my-3">
        <span> {{ rows }} Benutzer_innen gefunden </span>
      </div>

      <BTable
        id="user-table"
        hover
        :items="filteredUsers"
        :busy="loading"
        :fields="fields"
        primary-key="pk"
      >
        <div slot="table-busy" class="text-center text-danger my-2">
          <BSpinner class="align-middle mr-2"></BSpinner>
          <strong>Laden…</strong>
        </div>
        <div slot="name" slot-scope="{ value, item }">
          <b-link :to="{ name: 'UserDetail', params: { id: item.pk } }">
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
import { User } from "@/types";

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
      },
      {
        label: "Benutzername",
        key: "username",
        sortable: true
      }
    ] as TableFieldArray
  }),
  async mounted() {
    this.loading = true;
    try {
      await this.$store.dispatch("users/fetchAll");
    } catch (e) {
      this.$store.commit("alerts/add", {
        variant: "danger",
        text: "Benutzer konnten nicht geladen werden."
      });
    } finally {
      this.loading = false;
    }
  },
  computed: {
    filteredUsers(): User[] {
      let filtered: User[] = this.$store.getters["users/all"];
      if (this.nameFilter) {
        filtered = filtered.filter(
          (user) => user.name.toLowerCase().indexOf(this.nameFilter.toLowerCase()) > -1
        );
      }
      return filtered;
    },
    rows(): number {
      return this.filteredUsers.length;
    }
  }
});
</script>
