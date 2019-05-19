<template>
  <div class="mx-auto max-w-lg">
    <h1 class="text-center mb-6">
      <div class="text-2xl text-green-500">Konto Anlegen</div>
      <div class="text-base">zur JANUN-Seminarverwaltung</div>
    </h1>

    <div class="card border pt-10 mb-10">
      <UserForm
        :saving="saving"
        save-label="Anlegen &amp; Login"
        @save="signup"
      />
    </div>
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
  auth: false,
  layout: 'empty',
  middleware: 'guest',
  methods: {
    async signup(payload) {
      this.saving = true

      // rename password field for backend
      payload.password1 = payload.password
      payload.password2 = payload.password
      delete payload.password

      await this.$axios.$post('/auth/registration/', payload)
      await this.$auth.loginWith('local', {
        data: { username: payload.username, password: payload.password1 }
      })
      this.$router.push('/')
      this.saving = false
    }
  }
}
</script>
