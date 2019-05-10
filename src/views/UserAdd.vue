<template>
  <div class="mx-auto px-4 max-w-5xl">
    <h1 class="text-3xl text-green-500 font-bold">Konto anlegen</h1>

    <UserForm :saving="saving" @save="save" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import UserForm from '@/components/UserForm.vue';
import { User } from '../types';

export default Vue.extend({
  components: {
    UserForm
  },
  data: () => ({
    saving: false
  }),
  methods: {
    async save(form: User) {
      this.saving = true;
      try {
        await this.$store.dispatch('users/create', form);
        this.$toast('Konto erstellt');
        this.$router.push({ name: 'UserList' });
      } catch (error) {
        this.$toast('Erstellen fehlgeschlagen');
        // if (error.response.status === 400) {
        //   this.setServerErrors(error.response.data);
        // }
      } finally {
        this.saving = false;
      }
    }
  }
});
</script>
