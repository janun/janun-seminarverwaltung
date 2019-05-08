<template>
  <button class="btn btn-primary" @click="modalOpen = true">
    <slot>Neues Konto</slot>
    <BaseModal :show="modalOpen" @close="modalOpen = false" @show="focus">
      <h2 class="text-green-500 font-bold text-xl mb-5">Neues Konto</h2>

      <div
        v-if="serverErrors.length"
        class="my-4 px-3 py-2 bg-red-500 rounded-lg text-white text-sm"
      >
        <ul class="list-disc list-inside">
          <li v-for="(message, index) in serverErrors" :key="index">
            {{ message }}
          </li>
        </ul>
      </div>

      <BaseForm :validator="$v.form" @submit.prevent="save">
        <h2 class="text-green-500 mb-2 font-bold">Kontakt</h2>

        <BaseField label="Voller Name" name="name">
          <BaseInput ref="name" v-model="form.name" name="name" class="w-full" />
        </BaseField>

        <BaseField label="E-Mail-Adresse" name="email">
          <BaseInput v-model="form.email" type="email" name="email" class="w-full" />
        </BaseField>

        <BaseField label="Telefonnumer" optional name="telephone">
          <BaseInput v-model="form.telephone" name="telephone" type="tel" class="w-full" />
        </BaseField>

        <h2 class="text-green-500 mt-10 mb-2 font-bold">Konto</h2>

        <BaseField label="Anmeldename" name="username">
          <BaseInput v-model="form.username" name="username" class="w-full" />
        </BaseField>

        <BaseField label="Passwort" name="password">
          <BaseInput v-model="form.password" name="password" type="password" class="w-full" />
          <p class="text-sm">Min. 8 Zeichen</p>
        </BaseField>

        <h2 class="text-green-500 mt-10 mb-2 font-bold">Gruppen</h2>

        <BaseField label="Mitgliedschaften" name="janun_groups_pks">
          <GroupSelectMultiple v-model="form.janun_groups_pks" />
        </BaseField>

        <BaseField
          v-if="['Verwalter_in', 'Prüfer_in'].includes(form.role)"
          label="Hüte"
          name="group_hats_pks"
        >
          <GroupSelectMultiple v-model="form.group_hats_pks" />
        </BaseField>

        <h2 class="text-green-500 mt-10 mb-2 font-bold">Spezielles</h2>

        <BaseField label="Rolle" name="role">
          <BaseSelect v-model="form.role" :options="possibleRoles" />
        </BaseField>

        <BaseCheckbox v-model="form.is_reviewed">überprüft</BaseCheckbox>

        <div class="card-footer flex items-center">
          <button type="button" class="btn btn-tertiary" @click="modalOpen = false">
            Abbrechen
          </button>
          <button
            type="submit"
            class="btn btn-primary ml-auto"
            :class="{ 'btn-loading': saving }"
            :disabled="$v.form.$invalid"
            :title="$v.form.$invalid ? 'Fehler im Formular' : ''"
          >
            Anlegen
          </button>
        </div>
      </BaseForm>
    </BaseModal>
  </button>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseModal from '@/components/BaseModal.vue';
import BaseField from '@/components/BaseField.vue';
import BaseInput from '@/components/BaseInput.vue';
import BaseForm from '@/components/BaseForm.vue';
import BaseCheckbox from '@/components/BaseCheckbox.vue';
import BaseSelect from '@/components/BaseSelect.vue';
import GroupSelectMultiple from '@/components/GroupSelectMultiple.vue';
import { RuleDecl } from 'vue/types/options';
import { required, minLength, email } from 'vuelidate/lib/validators';

import store from '@/store/index.ts';
import { UserRole } from '../types';

async function usernameUnique(value: string): Promise<boolean> {
  if (!value || !(minLength(3) as any)(value)) {
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
    BaseModal,
    BaseField,
    BaseInput,
    BaseCheckbox,
    BaseForm,
    BaseSelect,
    GroupSelectMultiple
  },
  data: () => ({
    modalOpen: false,
    saving: false,
    serverErrors: [] as string[],
    form: {
      username: '',
      password: '',
      email: '',
      name: '',
      telephone: '',
      role: 'Teamer_in',
      janun_groups_pks: [],
      group_hats_pks: [],
      is_reviewed: false
    }
  }),
  validations: {
    form: {
      username: { required, minLength: minLength(3), unique: usernameUnique },
      password: { required, minLength: minLength(8) },
      email: { required, email, unique: emailUnique },
      name: { required },
      telephone: {},
      is_reviewed: {},
      role: {},
      janun_groups_pks: {},
      group_hats_pks: {}
    }
  } as RuleDecl,
  computed: {
    possibleRoles(): string[] {
      return Object.keys(UserRole);
    }
  },
  methods: {
    focus() {
      setTimeout(() => {
        (this.$refs.name as HTMLInputElement).focus();
      });
    },
    setServerErrors(data: any) {
      this.serverErrors = [].concat.apply([], Object.values(data));
    },
    async save() {
      this.saving = true;
      try {
        await this.$store.dispatch('users/create', this.form);
        this.$toast('Konto erstellt');
        this.modalOpen = false;
      } catch (error) {
        this.$toast('Erstellen fehlgeschlagen');
        if (error.response.status === 400) {
          this.setServerErrors(error.response.data);
        }
      } finally {
        this.saving = false;
      }
    }
  }
});
</script>
