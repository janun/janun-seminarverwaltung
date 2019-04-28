<template>
  <div class="card max-w-sm mx-auto relative">
    <h1 class="text-center mb-6 text-green-500 font-bold text-xl">Anmelden</h1>

    <div
      class="my-4 px-3 py-2 bg-red-500 rounded-lg text-white text-sm"
      v-if="nonFieldErrors && nonFieldErrors.length"
    >
      <span v-for="message in nonFieldErrors">
        {{ message }}
      </span>
    </div>

    <form @submit.prevent="login">
      <BaseField label="Benutzername">
        <BaseInput ref="username" name="username" v-model="form.username" class="w-full" />
      </BaseField>

      <BaseField label="Passwort">
        <BaseInput v-model="form.password" name="password" type="password" class="w-full" />
        <router-link class="btn tertiary" :to="{ name: 'PasswordReset' }">
          Passwort vergessen?
        </router-link>
      </BaseField>

      <div class="flex items-center">
        <router-link class="btn tertiary" :to="{ name: 'Signup' }">Konto anlegen</router-link>
        <button
          type="submit"
          class="ml-auto btn primary px-10"
          :class="{ loading: loading }"
          :disabled="!form.username || !form.password || loading"
        >
          Login
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseInput from '@/components/BaseInput.vue';
import BaseField from '@/components/BaseField.vue';

export default Vue.extend({
  components: {
    BaseInput,
    BaseField
  },
  data: () => ({
    loading: false,
    nonFieldErrors: [] as string[],
    form: {
      username: '',
      password: ''
    }
  }),
  methods: {
    async login() {
      this.loading = true;
      try {
        await this.$store.dispatch('auth/login', this.form);
        this.$router.push('/');
      } catch (error) {
        if (error.response.status === 400) {
          this.nonFieldErrors = error.response.data.non_field_errors;
        }
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    (this.$refs.username as HTMLInputElement).focus();
  }
});
</script>
