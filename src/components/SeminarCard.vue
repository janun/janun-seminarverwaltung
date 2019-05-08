<template>
  <router-link
    class="seminar block bg-white rounded shadow hover:shadow-md p-4 no-underline flex flex-col text-gray-600"
    style="min-height: 130px;"
    :to="{ name: 'SeminarDetail', params: { pk: seminar.pk } }"
  >
    <div class="flex items-baseline justify-between">
      <span class="text-xs text-grey-500">
        {{ seminar.start_date | date }} in {{ seminar.location }}
      </span>
      <StatusBadge :value="seminar.status" class="font-normal" />
    </div>

    <h3 class="mt-1 mb-2 leading-tight text-gray-800">{{ seminar.title }}</h3>

    <span v-if="seminar.group" class="text-xs">{{ seminar.group.name }}</span>

    <div class="flex items-baseline mt-auto">
      <span class="text-xs"> angemeldet am {{ seminar.created_at | date }} </span>
      <span
        class="text-xs ml-auto"
        :class="{
          'badge bg-red-500 text-white py-1 px-3': seminar.deadline_expired,
          'badge bg-yellow-500 text-white py-1 px-3': seminar.deadline_in_two_weeks
        }"
        :title="deadlineTitle"
        >Deadline {{ seminar.deadline | date }}</span
      >
    </div>
  </router-link>
</template>

<script lang="ts">
import Vue from 'vue';
import { Seminar } from '../types';
import StatusBadge from '@/components/StatusBadge.vue';
import { addDays } from '../utils/date';

export default Vue.extend({
  components: {
    StatusBadge
  },
  props: {
    seminar: { type: Object as () => Seminar, required: true }
  },
  computed: {
    deadlineTitle(): string {
      if (this.seminar.deadline_expired) {
        return 'Deadline zurm Einreichen der Abrechnung ist abgelaufen!';
      }
      if (this.seminar.deadline_in_two_weeks) {
        return 'Deadline zurm Einreichen der Abrechnung läuft bald ab!';
      }
      return '';
    }
  }
});
</script>
