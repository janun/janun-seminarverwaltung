<template>
  <div class="mx-auto px-4 max-w-5xl">
    <div v-if="loading" class="fullspinner" />

    <div v-if="object">
      <UserDeleteButton :user="object" class="btn-outline float-right" />
      <h1 class="text-3xl text-green-500 font-bold">{{ object.name }}</h1>

      <p>Erstellt: {{ object.created_at | date }}</p>
      <p>Letzte Änderung: {{ object.updated_at | date }}</p>
      <p>Letzter Besuch: {{ object.last_visit | date }}</p>

      <UserForm :saving="saving" :object="object" @save="save" />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import UserForm from '@/components/UserForm.vue';
import UserDeleteButton from '@/components/UserDeleteButton.vue';
import { User } from '../types';

export default Vue.extend({
  components: {
    UserForm,
    UserDeleteButton
  },
  props: {
    pk: { type: Number, required: true }
  },
  data: () => ({
    loading: true,
    saving: false
  }),
  computed: {
    object(): User {
      return this.$store.getters['users/byPk'](this.pk);
    }
  },
  async created() {
    this.loading = true;
    try {
      await this.$store.dispatch('users/fetchSingle', this.pk);
      document.title = this.object.name;
    } catch (error) {
      alert('Fehler beim Laden des Kontos');
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async save(form: User) {
      this.saving = true;
      try {
        await this.$store.dispatch('users/update', { pk: this.object.pk, data: form });
        this.$toast(`Konto ${this.object.name} geändert`);
      } catch (error) {
        this.$toast('Bearbeiten fehlgeschlagen');
        // if (error.response.status === 400) {
        //   (this as any).setServerErrors(error.response.data);
        // }
      } finally {
        this.saving = false;
      }
    }
  }
});
</script>
