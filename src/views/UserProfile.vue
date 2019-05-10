<template>
  <div class="mx-auto px-4 max-w-5xl">
    <h1 class="text-3xl text-green-500 font-bold">Dein Konto</h1>
    <UserForm :saving="saving" :object="user" @save="save" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import UserForm from '@/components/UserForm.vue';
import userMixin from '@/mixins/user.ts';
import { User } from '../types';

export default Vue.extend({
  components: {
    UserForm
  },
  mixins: [userMixin],
  data: () => ({
    saving: false
  }),
  methods: {
    async save(form: User) {
      this.saving = true;
      try {
        await this.$store.dispatch('auth/patchUser', form);
        this.$toast(`Profil geändert`);
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
