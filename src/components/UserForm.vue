<template>
  <BaseForm :validator="$v.form" @submit.prevent="save">
    <div class="flex flex-wrap mt-5">
      <div class="ml-auto">
        <button
          class="btn btn-primary mb-1 float-right"
          :class="{ 'btn-loading': saving }"
          type="submit"
          :disabled="!hasChanges || $v.form.$invalid || saving"
          :title="$v.form.$error ? 'Fehler im Formular' : !hasChanges ? 'Keine Änderungen' : ''"
        >
          Speichern
        </button>
        <p v-if="$v.form.$error" class="text-red-600">Fehler im Formular</p>
      </div>
    </div>

    <BaseFormSection label="Kontakt">
      <BaseField label="Voller Name" name="name">
        <BaseInput ref="name" v-model="form.name" name="name" class="w-full" />
      </BaseField>

      <BaseField label="E-Mail-Adresse" name="email">
        <BaseInput v-model="form.email" type="email" name="email" class="w-full" />
      </BaseField>

      <BaseField label="Telefonnumer" optional name="telephone">
        <BaseInput v-model="form.telephone" name="telephone" type="tel" class="w-full" />
      </BaseField>
    </BaseFormSection>

    <BaseFormSection label="Konto">
      <BaseField label="Anmeldename" name="username">
        <BaseInput v-model="form.username" name="username" class="w-full" />
      </BaseField>

      <BaseField label="Passwort" name="password">
        <BaseInput v-model="form.password" name="password" type="password" class="w-full" />
        <p class="text-sm">Min. 8 Zeichen. Leer lassen, um es nicht zu ändern.</p>
      </BaseField>
    </BaseFormSection>

    <BaseFormSection label="Gruppen">
      <BaseField label="Mitgliedschaften" name="janun_groups_pks">
        <GroupSelectMultiple v-model="form.janun_groups_pks" :readonly="!isStaff" />
      </BaseField>

      <BaseField
        v-if="['Verwalter_in', 'Prüfer_in'].includes(form.role)"
        label="Hüte"
        name="group_hats_pks"
      >
        <GroupSelectMultiple v-model="form.group_hats_pks" />
      </BaseField>
    </BaseFormSection>

    <BaseFormSection v-if="isStaff" label="Spezielles">
      <BaseField label="Rolle" name="role">
        <BaseSelect v-model="form.role" :options="possibleRoles" />
      </BaseField>

      <BaseField class="my-10">
        <BaseCheckbox v-model="form.is_reviewed" class="my-4">überprüft</BaseCheckbox>
        <p class="-mt-3">Nur überprüfte Konten können auf Gruppenseiten zugreifen.</p>
      </BaseField>
    </BaseFormSection>

    <div class="flex flex-wrap mt-5">
      <UserDeleteButton :user="object" class="btn-outline" />

      <div class="ml-auto">
        <button
          class="btn btn-primary mb-1 float-right"
          :class="{ 'btn-loading': saving }"
          type="submit"
          :disabled="!hasChanges || $v.form.$invalid || saving"
          :title="$v.form.$error ? 'Fehler im Formular' : !hasChanges ? 'Keine Änderungen' : ''"
        >
          Speichern
        </button>
        <p v-if="$v.form.$error" class="text-red-600">Fehler im Formular</p>
      </div>
    </div>
  </BaseForm>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseField from '@/components/BaseField.vue';
import BaseInput from '@/components/BaseInput.vue';
import BaseForm from '@/components/BaseForm.vue';
import BaseCheckbox from '@/components/BaseCheckbox.vue';
import BaseFormSection from '@/components/BaseFormSection.vue';
import BaseSelect from '@/components/BaseSelect.vue';
import UserDeleteButton from '@/components/UserDeleteButton.vue';
import GroupSelectMultiple from '@/components/GroupSelectMultiple.vue';
import { User, UserRole } from '../types';
import formMixin from '@/mixins/form.ts';
import userMixin from '@/mixins/user.ts';

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
    BaseField,
    BaseInput,
    BaseCheckbox,
    BaseForm,
    BaseSelect,
    UserDeleteButton,
    GroupSelectMultiple,
    BaseFormSection
  },
  mixins: [formMixin, userMixin],
  props: {
    object: { type: Object as () => User, required: true },
    saving: { type: Boolean, default: false }
  },
  data: () => ({
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
  created() {
    (this as any).copyFields();
    (this.$v.form as any).$touch();
    this.focus();
  },
  methods: {
    focus() {
      setTimeout(() => {
        (this.$refs.name as HTMLInputElement).focus();
      }, 100);
    },
    save() {
      this.$emit('save', this.form);
    }
  }
});
</script>
