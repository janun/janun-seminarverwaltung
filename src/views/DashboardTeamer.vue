<template>
  <div class="container mx-auto px-4">
    <router-link class="lg:float-right btn btn-primary" :to="{ name: 'SeminarApply' }">
      Seminar anmelden
    </router-link>
    <h1 class="text-green-500 text-2xl font-bold">Willkommen, {{ user.name }}!</h1>

    <h2 class="text-gray-800 font-bold text-xl mb-3 mt-10">Deine Gruppen</h2>
    <div v-if="user.janun_groups" class="flex flex-wrap -m-4">
      <div v-for="group in user.janun_groups" :key="group.pk" class="lg:w-1/3 sm:w-1/2 w-full p-4">
        <router-link
          class="seminar block bg-white rounded shadow hover:shadow-md p-4 no-underline flex flex-col"
          style="min-height: 75px;"
          :to="{ name: 'GroupDetail', params: { pk: group.pk } }"
        >
          <h3 class="mt-1 mb-2 leading-tight text-gray-800">{{ group.name }}</h3>
        </router-link>
      </div>
    </div>
    <div v-else>
      <p>Du bist nicht Mitglied in irgendwelchen JANUN-Gruppen.</p>
    </div>

    <h2 class="text-gray-800 font-bold text-xl mb-3 mt-10">Deine Seminare</h2>
    <SeminarCardList />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import userMixin from '@/mixins/user.ts';
import SeminarCardList from '@/components/SeminarCardList.vue';

export default Vue.extend({
  components: {
    SeminarCardList
  },
  mixins: [userMixin]
});
</script>
