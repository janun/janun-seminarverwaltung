<template>
  <div v-if="$auth.user" class="mx-auto max-w-5xl">
    <h1 class="text-2xl text-green-500 font-bold">Dein Profil</h1>
    <UserForm :object="$auth.user" :saving="saving" @save="save" />
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
  head() {
    return {
      title: 'Dein Profil'
    }
  },
  methods: {
    async save(payload) {
      this.saving = true
      await this.$axios.$patch(`/auth/user/`, payload)
      await this.$auth.fetchUser()
      this.saving = false
      this.$toast(`Profil gespeichert.`)
    }
  }
}
</script>
