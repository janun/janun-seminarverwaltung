<template>
  <button
    type="button"
    class="btn btn-outline text-red-600 hover:text-red-700 hover:bg-red-100 flex items-center"
    @click.prevent="modalOpen = true"
  >
    <slot>Konto Löschen</slot>

    <BaseModal :show="modalOpen" @close="modalOpen = false">
      <h1 class="text-red-600 font-bold text-2xl mb-6 flex items-center">
        {{ user.name }} wirklich löschen?
      </h1>

      <p>Möchtest Du das Konto „{{ user.name }}“ wirklich löschen?</p>

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
          class="btn btn-primary bg-red-600"
          :class="{ 'btn-loading': deleting }"
          @click="deleteUser"
        >
          Konto löschen
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
    user: { type: Object, required: true }
  },
  data: () => ({
    deleting: false,
    modalOpen: false,
    seminars: []
  }),
  // created() {
  //   this.seminars = this.$axios.$get(`/seminars/?owner_username=${this.user.username}`)
  // },
  methods: {
    async deleteUser() {
      try {
        this.deleting = true
        const name = this.user.name
        await this.$axios.$delete(`users/${this.user.username}/`)
        this.$toast(`Konto „${name}“ gelöscht.`)
        this.modalOpen = false
        this.$router.push('/users')
        this.$emit('deleted')
      } catch (error) {
        this.$nuxt.error(error)
      } finally {
        this.deleting = false
      }
    }
  }
}
</script>
