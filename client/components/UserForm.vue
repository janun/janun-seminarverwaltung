<template>
  <BaseForm :validator="$v.form" @submit.prevent="save">
    <div v-if="object" class="flex flex-wrap mt-5">
      <div class="ml-auto">
        <button
          class="btn btn-primary mb-1 float-right"
          :class="{ 'btn-loading': saving }"
          type="submit"
          :disabled="$v.form.$invalid || saving || !hasChanges"
        >
          {{ saveLabel }}
        </button>
        <p v-if="$v.form.$error" class="text-red-600">Fehler im Formular</p>
      </div>
    </div>

    <BaseFormSection label="Kontakt">
      <BaseField label="Voller Name" name="name">
        <BaseInput ref="name" v-model="form.name" name="name" class="w-full" />
      </BaseField>

      <BaseField label="E-Mail-Adresse" name="email">
        <BaseInput
          v-model="form.email"
          type="email"
          name="email"
          class="w-full"
        />
      </BaseField>

      <BaseField label="Telefonnumer" optional name="telephone">
        <BaseInput
          v-model="form.telephone"
          name="telephone"
          type="tel"
          class="w-full"
        />
      </BaseField>
    </BaseFormSection>

    <BaseFormSection label="Anmeldung">
      <BaseField label="Benutzername" name="username">
        <BaseInput v-model="form.username" name="username" class="w-full" />
      </BaseField>

      <BaseField label="Passwort" name="password">
        <BasePasswordInput
          v-model="form.password"
          name="password"
          type="password"
          class="w-full"
        />
        <p class="text-sm">
          Min. 8 Zeichen.
          <span v-if="object">Leer lassen, um es nicht zu ändern.</span>
        </p>
      </BaseField>
    </BaseFormSection>

    <BaseFormSection label="Gruppen">
      <p v-if="isSignup" class="mb-4">
        Bist Du Mitglied in einer oder mehreren JANUN-Gruppen?
      </p>
      <BaseField label="Mitgliedschaften" name="janun_groups_slugs">
        <GroupSelectMultiple
          v-model="form.janun_groups_slugs"
          :disabled="object && !$auth.user.has_staff_role"
        />
      </BaseField>

      <BaseField
        v-if="['Verwalter_in', 'Prüfer_in'].includes(form.role)"
        label="Hüte"
        name="group_hats_slugs"
      >
        <GroupSelectMultiple v-model="form.group_hats_slugs" />
      </BaseField>
    </BaseFormSection>

    <BaseFormSection
      v-if="$auth.loggedIn && $auth.user.has_staff_role"
      label="Spezielles"
    >
      <BaseField label="Rolle" name="role">
        <BaseSelect v-model="form.role" :options="possibleRoles" />
      </BaseField>

      <BaseField class="my-10">
        <BaseCheckbox v-model="form.is_reviewed" class="my-4"
          >überprüft</BaseCheckbox
        >
        <p class="-mt-3">
          Nur überprüfte Konten können auf Gruppenseiten zugreifen.
        </p>
      </BaseField>
    </BaseFormSection>

    <BaseFormSection v-if="isSignup" label="">
      <BaseCheckbox v-model="readDataProtection">
        Ich habe die
        <a
          class="underline"
          target="_blank"
          href="https://www.janun.de/documents/111/Datenverarbeitung_Seminarabrechnung.pdf"
        >
          Datenschutzbedingungen
        </a>
        gelesen und verstanden.
      </BaseCheckbox>
    </BaseFormSection>

    <div class="flex flex-wrap mt-5">
      <slot name="buttons" />
      <div class="ml-auto">
        <button
          class="btn btn-primary mb-1 float-right"
          :class="{ 'btn-loading': saving }"
          type="submit"
          :disabled="$v.$invalid || saving || !hasChanges"
        >
          {{ saveLabel }}
        </button>
        <p v-if="$v.form.$error" class="text-red-600">Fehler im Formular</p>
      </div>
    </div>
  </BaseForm>
</template>

<script>
import Vue from 'vue'
import BaseForm from '@/components/forms/BaseForm.vue'
import BaseFormSection from '@/components/forms/BaseFormSection.vue'
import BaseSelect from '@/components/forms/BaseSelect.vue'
import GroupSelectMultiple from '@/components/GroupSelectMultiple.vue'
import BasePasswordInput from '@/components/forms/BasePasswordInput.vue'

import {
  required,
  requiredIf,
  minLength,
  email
} from 'vuelidate/lib/validators'

import { checked, passwordNotOwned } from '@/utils/validators.js'

import { objectCompare } from '@/utils/object.js'

export default {
  components: {
    BaseForm,
    BaseSelect,
    GroupSelectMultiple,
    BaseFormSection,
    BasePasswordInput
  },
  props: {
    object: { type: Object, default: null },
    saving: { type: Boolean, default: false },
    saveLabel: { type: String, default: 'Speichern' },
    isSignup: { type: Boolean, default: false }
  },
  data: () => ({
    readDataProtection: false,
    form: {
      username: '',
      password: '',
      email: '',
      name: '',
      telephone: '',
      role: 'Teamer_in',
      janun_groups_slugs: [],
      group_hats_slugs: [],
      is_reviewed: false
    }
  }),
  validations() {
    const validations = {
      form: {
        username: {
          required,
          minLength: minLength(3),
          unique: this.usernameUniqueOrOld
        },
        password: {
          minLength: minLength(8),
          required: requiredIf(() => !this.object),
          passwordNotOwned
        },
        email: {
          required,
          email,
          unique: this.emailUniqueOrOld
        },
        name: { required },
        telephone: {},
        role: {},
        janun_groups_slugs: {},
        group_hats_slugs: {},
        is_reviewed: {}
      }
    }
    if (this.isSignup) {
      validations.readDataProtection = { checked: checked }
    }
    return validations
  },
  computed: {
    possibleRoles() {
      return ['Teamer_in', 'Prüfer_in', 'Verwalter_in']
    },
    hasChanges() {
      if (!this.object) {
        return true
      }
      return Object.keys(this.form).some(
        key => !objectCompare(this.form[key], this.object[key])
      )
    }
  },
  created() {
    if (this.object) {
      this.copyFields()
      this.$v.form.$touch()
    }
  },
  mounted() {
    this.$refs.name.focus()
  },
  methods: {
    copyFields() {
      this.$v.$reset()
      Object.keys(this.form).forEach(key =>
        Vue.set(this.form, key, this.object[key])
      )
    },
    save() {
      this.$emit('save', this.form)
    },
    async usernameUniqueOrOld(value) {
      if (!value || !minLength(3)(value)) {
        return true
      }
      if (this.object && value === this.object.username) {
        return true
      }
      const data = await this.$axios.$get('auth/username-exists/', {
        params: { username: value }
      })
      return !data.exists
    },
    async emailUniqueOrOld(value) {
      if (!value || !email(value)) {
        return true
      }
      if (this.object && value === this.object.email) {
        return true
      }
      const data = await this.$axios.$get('auth/email-exists/', {
        params: { email: value }
      })
      return !data.exists
    }
  }
}
</script>
