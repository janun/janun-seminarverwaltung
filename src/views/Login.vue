<template>
  <div class="card max-w-xs mx-auto relative">
    <h1 class="text-2xl mb-4 text-green-500 -mt-2">Login</h1>

    <div class="fullspinner" v-if="loading"></div>

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
        <BaseInput ref="username" v-model="form.username" class="w-full" />
      </BaseField>

      <BaseField label="Passwort">
        <BaseInput v-model="form.password" type="password" class="w-full" />
      </BaseField>

      <div class="card-footer flex items-center">
        <router-link class="btn tertiary" :to="{ name: 'Signup' }">Signup</router-link>
        <button
          type="submit"
          class="ml-auto btn primary"
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
