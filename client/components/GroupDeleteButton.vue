<template>
  <button
    type="button"
    class="text-red-500 hover:text-red-700 focus:text-red-700 flex items-center"
    @click.prevent="modalOpen = true"
  >
    <slot>Gruppe Löschen</slot>

    <BaseModal :show="modalOpen" @close="modalOpen = false">
      <h1 class="text-red-500 font-bold text-2xl mb-6 flex items-center">
        {{ group.name }} wirklich löschen?
      </h1>

      <p>Möchtest Du die Gruppe „{{ group.name }}“ wirklich löschen?</p>

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
          @click="deleteGroup"
        >
          Gruppe löschen
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
    group: { type: Object, required: true }
  },
  data: () => ({
    deleting: false,
    modalOpen: false,
    seminars: []
  }),
  // created() {
  //   this.seminars = this.$axios.$get(`/seminars/?group_pk=${this.group.pk}`)
  // },
  methods: {
    async deleteGroup() {
      this.deleting = true
      const name = this.group.name
      await this.$axios.$delete(`groups/${this.group.pk}/`)
      this.$toast(`Gruppe „${name}“ gelöscht.`)
      this.modalOpen = false
      this.$router.push('/groups')
      this.$emit('deleted')
      this.deleting = false
    }
  }
}
</script>
