<template>
  <BaseModal :show="show" @close="close">
    <h2 class="text-green-500 font-bold text-xl mb-5">{{ object.name }} editieren</h2>

    <div v-if="serverErrors.length" class="my-4 px-3 py-2 bg-red-500 rounded-lg text-white text-sm">
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
        <p class="text-sm">Min. 8 Zeichen. Leer lassen, um es nicht zu ändern.</p>
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

      <BaseCheckbox v-model="form.is_reviewed" class="my-4">überprüft</BaseCheckbox>

      <UserDeleteButton :user="object" class="my-5 btn-secondary" @deleted="close" />

      <div class="card-footer flex items-center">
        <button type="button" class="btn btn-tertiary" @click="close">
          Abbrechen
        </button>
        <button
          type="submit"
          class="btn btn-primary ml-auto"
          :class="{ 'btn-loading': saving }"
          :disabled="$v.form.$invalid"
          :title="$v.form.$invalid ? 'Fehler im Formular' : ''"
        >
          Speichern
        </button>
      </div>
    </BaseForm>
  </BaseModal>
</template>

<script lang="ts">
import Vue from 'vue';
import { User, UserRole } from '@/types.ts';
import BaseModal from '@/components/BaseModal.vue';
import BaseField from '@/components/BaseField.vue';
import BaseInput from '@/components/BaseInput.vue';
import BaseForm from '@/components/BaseForm.vue';
import BaseCheckbox from '@/components/BaseCheckbox.vue';
import BaseSelect from '@/components/BaseSelect.vue';
import UserDeleteButton from '@/components/UserDeleteButton.vue';
import GroupSelectMultiple from '@/components/GroupSelectMultiple.vue';

import { RuleDecl } from 'vue/types/options';
import { required, minLength, email } from 'vuelidate/lib/validators';

import store from '@/store/index.ts';

function usernameUniqueOrOld(oldValue: string) {
  return async function usernameUnique(value: string): Promise<boolean> {
    if (!value || !(minLength(3) as any)(value)) {
      return true;
    }
    if (value === oldValue) {
      return true;
    }
    const exists = await store.dispatch('auth/usernameExists', value);
    return !exists;
  };
}

function emailUniqueOrOld(oldValue: string) {
  return async function emailUnique(value: string): Promise<boolean> {
    if (!value || !(email as any)(value)) {
      return true;
    }
    if (value === oldValue) {
      return true;
    }
    const exists = await store.dispatch('auth/emailExists', value);
    return !exists;
  };
}

export default Vue.extend({
  components: {
    BaseModal,
    BaseField,
    BaseInput,
    BaseCheckbox,
    BaseForm,
    BaseSelect,
    UserDeleteButton,
    GroupSelectMultiple
  },
  model: {
    prop: 'show',
    event: 'close'
  },
  props: {
    show: { type: Boolean, default: false },
    object: { type: Object as () => User, required: true }
  },
  data: () => ({
    saving: false,
    serverErrors: [] as string[],
    form: {
      username: '',
      password: '',
      email: '',
      name: '',
      telephone: '',
      role: '',
      janun_groups_pks: [],
      group_hats_pks: [],
      is_reviewed: true
    }
  }),
  validations(): RuleDecl {
    return {
      form: {
        username: {
          required,
          minLength: minLength(3),
          unique: usernameUniqueOrOld(this.object.username)
        },
        password: { minLength: minLength(8) },
        email: { required, email, unique: emailUniqueOrOld(this.object.email) },
        name: { required },
        telephone: {},
        role: {},
        janun_groups_pks: {},
        group_hats_pks: {},
        is_reviewed: {}
      }
    };
  },
  computed: {
    possibleRoles(): string[] {
      return Object.keys(UserRole);
    }
  },
  watch: {
    show(show) {
      if (show) {
        this.copyFields();
        (this.$v.form as any).$touch();
        this.focus();
      }
    }
  },
  methods: {
    focus() {
      setTimeout(() => {
        (this.$refs.name as HTMLInputElement).focus();
      }, 100);
    },
    setServerErrors(data: any) {
      this.serverErrors = [].concat.apply([], Object.values(data));
    },
    close() {
      this.serverErrors = [];
      this.$emit('close', false);
    },
    async save() {
      this.saving = true;
      try {
        await this.$store.dispatch('users/update', { pk: this.object.pk, data: this.form });
        this.$toast(`Konto ${this.object.name} geändert`);
        this.close();
      } catch (error) {
        this.$toast('Bearbeiten fehlgeschlagen');
        if (error.response.status === 400) {
          this.setServerErrors(error.response.data);
        }
      } finally {
        this.saving = false;
      }
    },
    copyFields(): void {
      this.$v.$reset();
      if (this.object) {
        for (const key in this.form) {
          if (this.form.hasOwnProperty(key)) {
            Vue.set(this.form, key, this.object[key as keyof User]);
          }
        }
      }
    }
  }
});
</script>
