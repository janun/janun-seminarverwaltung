<template>
  <button
    type="button"
    class="text-red-500 hover:text-red-700 focus:text-red-700 flex items-center"
    @click.prevent="modalOpen = true"
  >
    <slot>Seminar löschen</slot>

    <BaseModal :show="modalOpen" @close="modalOpen = false">
      <h1 class="text-red-500 font-bold text-2xl mb-6 flex items-center">
        Seminar wirklich löschen?
      </h1>

      <p>Möchtest Du das Seminar „{{ seminar.title }}“ wirklich löschen?</p>

      <div class="card-footer flex justify-between mt-6">
        <button type="button" class="btn tertiary" @click="modalOpen = false">
          Abbrechen
        </button>
        <button
          type="button"
          class="btn primary bg-red-500"
          :class="{ loading: deleting }"
          @click="deleteSeminar"
        >
          Seminar löschen
        </button>
      </div>
    </BaseModal>
  </button>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseModal from '@/components/BaseModal.vue';

export default Vue.extend({
  components: {
    BaseModal
  },
  props: {
    seminar: { type: Object, required: true }
  },
  data: () => ({
    deleting: false,
    modalOpen: false
  }),
  methods: {
    async deleteSeminar() {
      this.deleting = true;
      try {
        const title = this.seminar.title;
        await this.$store.dispatch('seminars/delete', this.seminar.pk);
        this.$toast(`Seminar „${title}“ gelöscht.`);
        this.$router.push('/');
      } catch (error) {
        this.$toast('Fehler beim Löschen des Seminars', { type: 'error' });
        throw error;
      } finally {
        this.deleting = false;
      }
    }
  }
});
</script>
