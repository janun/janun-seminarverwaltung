<template>
  <div>
    <h1 class="title">Benutzer_innen</h1>

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

    <b-table :data="filteredUsers" hoverable default-sort="name" :loading="loading">
      <template slot-scope="{ row }">
        <b-table-column field="name" label="Name" sortable>
          <router-link :to="{ name: 'UserDetail', params: { pk: row.pk } }">
            {{ row.name }}
          </router-link>
        </b-table-column>
        <b-table-column field="username" label="Benutzername" sortable>
          {{ row.username }}
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { User } from '@/types';

export default Vue.extend({
  data: () => ({
    loading: true,
    nameFilter: ''
  }),
  async mounted() {
    this.loading = true;
    try {
      await this.$store.dispatch('users/fetchAll');
    } catch (e) {
      this.$store.commit('alerts/add', {
        variant: 'danger',
        text: 'Benutzer konnten nicht geladen werden.'
      });
    } finally {
      this.loading = false;
    }
    (this.$refs.nameFilter as HTMLFormElement).focus();
  },
  computed: {
    filteredUsers(): User[] {
      let filtered: User[] = this.$store.getters['users/all'];
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
