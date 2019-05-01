<template>
  <div class="card max-w-md mx-auto relative">
    <h1 class="text-center mb-10 text-green-500 font-bold text-xl">Konto Anlegen</h1>

    <div class="my-4 px-3 py-2 bg-red-500 rounded-lg text-white text-sm" v-if="serverErrors.length">
      <ul class="list-disc list-inside">
        <li v-for="(message, index) in serverErrors" :key="index">
          {{ message }}
        </li>
      </ul>
    </div>

    <form @submit.prevent="signup">
      <h2 class="text-green-500 mb-2 font-bold">Kontakt-Daten</h2>

      <BaseField label="Voller Name" name="name">
        <BaseInput ref="name" name="name" v-model="form.name" class="w-full" />
      </BaseField>

      <BaseField label="E-Mail-Adresse" name="email">
        <BaseInput type="email" name="email" v-model="form.email" class="w-full" />
        <p class="text-sm">Für Nachrichten zu Deinen Seminaren</p>
      </BaseField>

      <BaseField label="Telefonnumer" optional name="telephone">
        <BaseInput v-model="form.telephone" name="telephone" type="tel" class="w-full" />
        <p class="text-sm">Für dringende Probleme mit Deinem Seminar</p>
      </BaseField>

      <h2 class="text-green-500 mt-10 mb-2 font-bold">Account-Daten</h2>

      <BaseField label="Benutzername" name="username">
        <BaseInput v-model="form.username" name="username" class="w-full" />
      </BaseField>

      <BaseField label="Passwort" name="password1">
        <BaseInput v-model="form.password1" name="password" type="password" class="w-full" />
        <p class="text-sm">Min. 8 Zeichen</p>
      </BaseField>

      <div class="flex items-center mt-12">
        <button
          type="submit"
          :title="$v.form.$invalid ? 'Fülle alle Felder richtig aus' : ''"
          class="btn btn-primary ml-auto px-10"
          :class="{ 'btn-loading': loading }"
          :disabled="$v.form.$invalid || loading"
        >
          Konto Anlegen
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseInput from '@/components/BaseInput.vue';
import BaseField from '@/components/BaseField.vue';

import { required, minLength, email } from 'vuelidate/lib/validators';
import store from '@/store/index.ts';

async function usernameUnique(value: string): Promise<boolean> {
  if (!value || !(minLength(4) as any)(value)) {
    return true;
  }
  const exists = await store.dispatch('auth/usernameExists', value);
  return !exists;
}

async function emailUnique(value: string): Promise<boolean> {
  if (!value || !(email as any)(value)) {
    return true;
  }
  const exists = await store.dispatch('auth/emailExists', value);
  return !exists;
}

export default Vue.extend({
  components: {
    BaseInput,
    BaseField
  },
  provide(): object {
    return {
      formValidator: this.$v.form
    };
  },
  data: () => ({
    loading: false,
    serverErrors: [] as string[],
    form: {
      name: '',
      email: '',
      username: '',
      password1: '',
      telephone: ''
    }
  }),
  validations: {
    form: {
      name: { required },
      email: { required, email, unique: emailUnique },
      username: { required, minLength: minLength(4), unique: usernameUnique },
      password1: { required, minLength: minLength(8) },
      telephone: {}
    }
  },
  methods: {
    setServerErrors(data: any) {
      this.serverErrors = [].concat.apply([], Object.values(data));
    },
    async signup() {
      this.loading = true;
      try {
        await this.$store.dispatch('auth/signup', this.form);
        this.$router.push('/');
      } catch (error) {
        if (error.response.status === 400) {
          this.setServerErrors(error.response.data);
        }
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    (this.$refs.name as HTMLInputElement).focus();
  }
});
</script>
