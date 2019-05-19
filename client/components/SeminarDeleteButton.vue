<template>
  <button
    type="button"
    class="btn-outline text-red-500 hover:text-red-700 focus:text-red-700 flex items-center"
    @click.prevent="modalOpen = true"
  >
    <slot>Seminar löschen</slot>

    <BaseModal :show="modalOpen" @close="modalOpen = false">
      <h1 class="text-red-500 font-bold text-2xl mb-6 flex items-center">
        Seminar wirklich löschen?
      </h1>

      <p>Möchtest Du das Seminar „{{ seminar.title }}“ wirklich löschen?</p>

      <div class="card-footer flex justify-between mt-6">
        <button
          type="button"
          class="btn btn-tertiary"
          @click="modalOpen = false"
        >
          Abbrechen
        </button>
        <button
          type="button"
          class="btn btn-primary bg-red-500"
          :class="{ 'btn-loading': deleting }"
          @click="deleteSeminar"
        >
          Seminar löschen
        </button>
      </div>
    </BaseModal>
  </button>
</template>

<script>
import BaseModal from '@/components/BaseModal.vue'

export default {
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
      this.deleting = true
      const title = this.seminar.title
      await this.$axios.$delete(`seminars/${this.seminar.pk}/`)
      this.deleting = false
      this.$router.push('/seminars')
      this.$toast(`Seminar „${title}“ gelöscht.`)
    }
  }
}
</script>
