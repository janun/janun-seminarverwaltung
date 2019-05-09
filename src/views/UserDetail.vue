<template>
  <div class="mx-auto px-4 max-w-5xl">
    <div v-if="loading" class="fullspinner" />

    <div v-if="object">
      <h1 class="text-3xl text-green-500 font-bold">{{ object.name }}</h1>

      <UserForm :object="object" />
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
  props: {
    pk: { type: Number, required: true }
  },
  data: () => ({
    loading: true
  }),
  computed: {
    object(): User | undefined {
      return this.$store.getters['users/byPk'](this.pk);
    }
  },
  async created() {
    this.loading = true;
    try {
      await this.$store.dispatch('users/fetchSingle', this.pk);
      if (this.object) {
        document.title = this.object.name;
      }
    } catch (error) {
      alert('Fehler beim Laden des Kontos');
    } finally {
      this.loading = false;
    }
  }
});
</script>
