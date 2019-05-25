<template>
  <div class="mx-auto max-w-4xl">
    <h1 class="text-xl text-green-500 font-bold mb-5">Neues Konto</h1>
    <UserForm :saving="saving" @save="save" />
  </div>
</template>

<script>
import UserForm from '@/components/UserForm.vue'

export default {
  components: {
    UserForm
  },
  data() {
    return {
      saving: false
    }
  },
  meta() {
    return {
      title: 'Neues Konto'
    }
  },
  methods: {
    async save(payload) {
      this.saving = true
      try {
        const data = await this.$axios.$post(`/users/`, payload)
        this.$toast(`Konto ${data.name} erstellt`)
        this.$router.push(`/users/${data.pk}`)
      } catch (error) {
        this.$nuxt.error(error)
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
