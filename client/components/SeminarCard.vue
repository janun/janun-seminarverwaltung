<template>
  <nuxt-link
    class="seminar block bg-white rounded shadow hover:shadow-md p-4 no-underline flex flex-col text-gray-600"
    style="min-height: 130px;"
    :to="`/seminars/${seminar.uuid}`"
  >
    <div class="flex items-baseline justify-between mb-1">
      <span class="text-xs text-grey-600">
        {{ seminar.start_date | date }} in {{ seminar.location }}
      </span>
      <StatusBadge :value="seminar.status" class="font-normal" />
    </div>

    <h3 class="mt-1 mb-2 leading-tight text-gray-800 font-bold">
      {{ seminar.title }}
    </h3>

    <span v-if="seminar.group" class="text-xs mb-1">
      Gruppe: {{ seminar.group.name }}
    </span>

    <div class="flex items-baseline mt-auto">
      <span class="text-xs">
        angemeldet am {{ seminar.created_at | date }}
      </span>
      <span
        class="text-xs ml-auto"
        :class="{
          'badge bg-red-100 text-red-600': seminar.deadline_expired,
          'badge bg-yellow-100 text-yellow-600': seminar.deadline_in_two_weeks
        }"
        :title="deadlineTitle"
        >Deadline {{ seminar.deadline | date }}</span
      >
    </div>
  </nuxt-link>
</template>

<script>
import StatusBadge from '@/components/StatusBadge.vue'

export default {
  components: {
    StatusBadge
  },
  props: {
    seminar: { type: Object, required: true }
  },
  computed: {
    deadlineTitle() {
      if (this.seminar.deadline_expired) {
        return 'Deadline zurm Einreichen der Abrechnung ist abgelaufen!'
      }
      if (this.seminar.deadline_in_two_weeks) {
        return 'Deadline zurm Einreichen der Abrechnung läuft bald ab!'
      }
      return ''
    }
  }
}
</script>
