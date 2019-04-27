<template>
  <div class="container mx-auto px-4">
    <h1 class="text-green-500 text-2xl font-semibold">Willkommen, {{ user.name }}</h1>

    <router-link class="lg:float-right btn primary my-3s" :to="{ name: 'SeminarApply' }">
      Seminar anmelden
    </router-link>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import userMixin from '@/mixins/user.ts';

export default Vue.extend({
  mixins: [userMixin]
});
</script>
