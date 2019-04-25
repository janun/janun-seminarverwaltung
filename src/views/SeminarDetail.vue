<template>
  <div class="mx-auto px-4" style="max-width: 50rem">
    <div class="fullspinner" v-if="loading" />

    <div v-if="object">
      <h1 class="text-2xl text-green-500 font-bold">{{ object.title }}</h1>

      <div class="mb-5">
        Am {{ object.start_date | date }}
        <span v-if="object.location">in {{ object.location }}</span>
      </div>

      <div class="text-gray-700 text-sm">
        <div class="">Deadline zur Abrechnung: {{ object.deadline | date }}</div>
        <div>
          angemeldet von
          <router-link
            class="text-green-500"
            :to="{ name: 'UserDetail', params: { pk: object.owner.pk } }"
          >
            {{ object.owner.name }}
          </router-link>
          am {{ object.created_at | date }}
          <br />
          zuletzt geändert am {{ object.updated_at | date }}
        </div>
        <div v-if="object.group">
          Gruppe:
          <router-link
            class="text-green-500"
            :to="{ name: 'GroupDetail', params: { pk: object.group.pk } }"
          >
            {{ object.group.name }}
          </router-link>
        </div>
      </div>

      <SeminarForm ref="seminarForm" :object="object" />

      <div class="flex flex-wrap mt-20">
        <div class="w-full md:w-1/3 mb-5">
          <h2 class="text-green-500 font-bold text-lg">Kommentare</h2>
        </div>

        <div class="w-full md:w-2/3">
          <CommentList class="w-full" :seminarId="pk" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { Seminar } from '@/types';

import SeminarForm from '@/components/SeminarForm.vue';
import SeminarStatus from '@/components/SeminarStatus.vue';
import CommentList from '@/components/CommentList.vue';

export default Vue.extend({
  components: {
    SeminarForm,
    SeminarStatus,
    CommentList
  },
  props: {
    pk: { type: Number, required: true }
  },
  data: () => ({
    loading: true,
    saving: false
  }),
  computed: {
    object(): Seminar | undefined {
      return this.$store.getters['seminars/byPk'](this.pk);
    }
  },
  async created() {
    this.loading = true;
    try {
      await this.$store.dispatch('seminars/fetchSingle', this.pk);
      // (this.$refs.seminarForm as any).copyFields();
    } catch (error) {
      alert('Fehler beim Laden des Seminars');
    } finally {
      this.loading = false;
    }
  }
});
</script>
