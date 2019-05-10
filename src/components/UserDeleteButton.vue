<template>
  <button
    type="button"
    class="text-red-500 hover:text-red-700 focus:text-red-700 flex items-center"
    @click.prevent="modalOpen = true"
  >
    <slot>Konto Löschen</slot>

    <BaseModal :show="modalOpen" @close="modalOpen = false">
      <h1 class="text-red-500 font-bold text-2xl mb-6 flex items-center">
        {{ user.name }} wirklich löschen?
      </h1>

      <p>Möchtest Du das Konto „{{ user.name }}“ wirklich löschen?</p>

      <div class="card-footer flex justify-between mt-6">
        <button type="button" class="btn btn-tertiary" @click="modalOpen = false">
          Abbrechen
        </button>
        <button
          type="button"
          class="btn btn-primary bg-red-500"
          :class="{ 'btn-loading': deleting }"
          @click="deleteUser"
        >
          Konto löschen
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
    user: { type: Object, required: true }
  },
  data: () => ({
    deleting: false,
    modalOpen: false
  }),
  methods: {
    async deleteUser() {
      this.deleting = true;
      try {
        const name = this.user.name;
        await this.$store.dispatch('users/delete', this.user.pk);
        this.$toast(`Konto „${name}“ gelöscht.`);
        this.modalOpen = false;
        this.$router.push({ name: 'UserList' });
        this.$emit('deleted');
      } catch (error) {
        this.$toast('Fehler beim Löschen des Kontos', { type: 'error' });
        throw error;
      } finally {
        this.deleting = false;
      }
    }
  }
});
</script>
