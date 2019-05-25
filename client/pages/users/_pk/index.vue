<template>
  <div class="mx-auto max-w-5xl">
    <div class="flex flex-wrap items-center">
      <h1 class="text-2xl text-green-500 font-bold">{{ user.name }}</h1>
      <UserDeleteButton :user="user" class="ml-auto" />
    </div>

    <p>Erstellt: {{ user.created_at | date }}</p>
    <p>Letzte Änderung: {{ user.updated_at | date }}</p>
    <p>Letzter Besuch: {{ user.last_visit | date }}</p>

    <UserForm :object="user" :saving="saving" @save="save" />
  </div>
</template>

<script>
import UserForm from '@/components/UserForm.vue'
import UserDeleteButton from '@/components/UserDeleteButton.vue'

export default {
  components: {
    UserForm,
    UserDeleteButton
  },
  data() {
    return {
      saving: false,
      user: {}
    }
  },
  head() {
    return {
      title: this.user.name
    }
  },
  async asyncData({ $axios, params }) {
    const data = await $axios.$get(`/users/${params.pk}/`)
    return { user: data }
  },
  methods: {
    async save(payload) {
      this.saving = true
      try {
        this.user = await this.$axios.$put(`/users/${this.user.pk}/`, payload)
        this.$toast(`Änderungen an ${this.user.name} gespeichert.`)
      } catch (error) {
        this.$nuxt.error(error)
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
