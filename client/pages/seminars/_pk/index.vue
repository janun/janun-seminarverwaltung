<template>
  <div class="mx-auto max-w-4xl">
    <SeminarDeleteButton
      v-if="$auth.user.has_staff_role"
      :seminar="seminar"
      class="float-right"
    />
    <h1 class="text-green-500 font-bold text-2xl mb-5">{{ seminar.title }}</h1>

    <div class="mb-5">
      Am {{ seminar.start_date | date }}
      <span v-if="seminar.location">in {{ seminar.location }}</span>
    </div>

    <div class="text-sm">
      <span v-if="seminar.owner">
        von
        <nuxt-link class="text-green-500" :to="`/users/${seminar.owner.pk}`">
          {{ seminar.owner.name }}.
        </nuxt-link>
      </span>
      erstellt {{ seminar.created_at | date }}, geändert
      {{ seminar.updated_at | date }}
    </div>

    <div v-if="seminar.group" class="text-sm">
      Gruppe:
      <nuxt-link class="text-green-500" :to="`/groups/${seminar.group.pk}`">
        {{ seminar.group.name }}
      </nuxt-link>
    </div>

    <div class="text-sm">
      Deadline: {{ seminar.deadline | date }}
      <span v-if="seminar.deadline_expired" class="badge bg-red-300 ml-1">
        abgelaufen!
      </span>
      <span
        v-if="seminar.deadline_in_two_weeks"
        class="badge bg-yellow-300 ml-1"
      >
        bald
      </span>
    </div>

    <SeminarForm :seminar="seminar" :saving="saving" @save="save" />

    <h2 class="text-green-500 font-bold mb-3 text-xl">Kommentare</h2>
    <CommentList :seminar-pk="seminar.pk" />
  </div>
</template>

<script>
import SeminarForm from '@/components/SeminarForm.vue'
import SeminarDeleteButton from '@/components/SeminarDeleteButton.vue'
import CommentList from '@/components/CommentList.vue'

export default {
  components: {
    SeminarForm,
    SeminarDeleteButton,
    CommentList
  },
  data() {
    return {
      seminar: {},
      saving: false
    }
  },
  head() {
    return {
      title: this.seminar.title
    }
  },
  async asyncData({ $axios, params }) {
    const data = await $axios.$get(`/seminars/${params.pk}/`)
    return { seminar: data }
  },
  methods: {
    async save(payload) {
      this.saving = true
      const data = await this.$axios.$patch(
        `/seminars/${this.seminar.pk}/`,
        payload
      )
      this.seminar = data
      this.saving = false
    }
  }
}
</script>
