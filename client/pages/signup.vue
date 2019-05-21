<template>
  <div class="mx-auto max-w-lg">
    <h1 class="text-center mb-6">
      <div class="text-2xl text-green-500">Konto Anlegen</div>
      <div class="text-base">zur JANUN-Seminarverwaltung</div>
    </h1>

    <div class="card border pt-10 mb-10">
      <p v-if="nonFieldErrors" class="text-red-500 font-bold italic my-3">
        {{ nonFieldErrors.join(', ') }}
      </p>
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
      errors: undefined,
      nonFieldErrors: undefined,
      saving: false
    }
  },
  provide() {
    return {
      serverErrorsGetter: () => this.errors
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

      try {
        await this.$axios.$post('/auth/registration/', payload)
        await this.$auth.loginWith('local', {
          data: { username: payload.username, password: payload.password1 }
        })
        this.$router.push('/')
      } catch (error) {
        if (error.response.status === 400) {
          this.errors = error.response.data
          this.nonFieldErrors = error.response.data.non_field_errors
        } else {
          this.error({ statusCode: 500, message: 'Server Fehler' })
        }
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
