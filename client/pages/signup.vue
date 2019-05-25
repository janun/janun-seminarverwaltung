<template>
  <div class="mx-auto max-w-xl px-4 mt-5 sm:mt-10 sm:card sm:px-10">
    <h1 class="sm:text-center mb-6 sm:mb-12 text-2xl font-bold text-green-500">
      Konto Anlegen
      <div class="font-normal text-gray-600 text-sm">
        zur JANUN-Seminarverwaltung
      </div>
    </h1>

    <p v-if="nonFieldErrors" class="text-red-600 font-bold italic my-3">
      {{ nonFieldErrors.join(', ') }}
    </p>

    <UserForm
      :saving="saving"
      save-label="Anlegen &amp; Anmelden"
      @save="signup"
    >
      <nuxt-link slot="buttons" class="btn btn-secondary" to="/login">
        Anmeldung
      </nuxt-link>
    </UserForm>
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
        if (error.response && error.response.status === 400) {
          this.errors = error.response.data
          this.nonFieldErrors = error.response.data.non_field_errors
        } else {
          this.$nuxt.error(error)
        }
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
