<template>
  <div class="max-w-lg mx-auto ">
    <h1 class="text-center mb-6">
      <div class="text-2xl text-green-500">Konto Anlegen</div>
      <div class="text-base">zur JANUN-Seminarverwaltung</div>
    </h1>

    <div class="card pt-10">
      <UserForm :saving="saving" save-label="Konto Anlegen" @save="signup" />
    </div>
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
    async signup(form: User) {
      this.saving = true;
      try {
        await this.$store.dispatch('auth/signup', form);
        this.$router.push('/');
      } catch (error) {
        this.$toast('Konto Erstellen Fehlgeschlagen');
      } finally {
        this.saving = false;
      }
    }
  }
});
</script>
