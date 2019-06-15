<template>
  <div class="mx-auto sm:max-w-sm mt-5 sm:mt-10 px-4">
    <div class="md:card">
      <h1
        class="sm:text-center font-bold mb-6 sm:mb-12 text-2xl text-green-500"
      >
        Anmeldung
        <div class="font-normal text-gray-600 text-sm">
          zur JANUN-Seminarverwaltung
        </div>
      </h1>

      <p v-if="nonFieldErrors" class="text-red-600 font-bold italic my-3">
        {{ nonFieldErrors.join(', ') }}
      </p>

      <form method="post" @submit.prevent="login">
        <BaseField label="Benutzername" name="username">
          <BaseInput
            id="username"
            ref="username"
            v-model="form.username"
            name="username"
            class="w-full"
          />
        </BaseField>

        <BaseField label="Passwort" name="password">
          <BasePasswordInput
            id="password"
            v-model="form.password"
            name="password"
            class="w-full"
          />
        </BaseField>

        <div class="flex flex-wrap items-center mt-10">
          <nuxt-link class="btn btn-secondary" to="/signup">
            Konto anlegen
          </nuxt-link>

          <button
            type="submit"
            class="btn btn-primary ml-auto px-10"
            :class="{ 'btn-loading': loading }"
            :disabled="!form.username || !form.password || loading"
          >
            Login
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import BasePasswordInput from '@/components/forms/BasePasswordInput.vue'

export default {
  components: {
    BasePasswordInput
  },
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      loading: false,
      errors: undefined,
      nonFieldErrors: undefined
    }
  },
  head() {
    return {
      title: 'Anmeldung'
    }
  },
  provide() {
    return {
      serverErrorsGetter: () => this.errors
    }
  },
  layout: 'empty',
  mounted() {
    this.$refs.username.focus()
  },
  methods: {
    async login() {
      this.loading = true
      try {
        await this.$auth.loginWith('local', { data: this.form })
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.errors = error.response.data
          this.nonFieldErrors = error.response.data.non_field_errors
        } else {
          this.$nuxt.error(error)
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
