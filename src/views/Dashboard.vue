<template>
  <div class="container mx-auto px-4">
    <h1 class="text-green-500 text-2xl font-semibold">Willkommen, {{ user.name }}</h1>
    <button class="btn secondary" @click="showModal = true">Zeige Modalfenster</button>
    <BaseModal :show="showModal" @close="showModal = false">
      <h2 class="text-green-500 font-bold text-2xl">Dies ist ein Modalfenster</h2>
      <p>… und ein bisschen Text.</p>
    </BaseModal>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import userMixin from '@/mixins/user.ts';
import BaseModal from '../components/BaseModal.vue';

export default Vue.extend({
  components: {
    BaseModal
  },
  data: () => ({
    showModal: false
  }),
  mixins: [userMixin]
});
</script>
