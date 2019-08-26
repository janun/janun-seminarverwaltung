<template>
  <BaseForm :validator="$v.form" @submit.prevent="save">
    <BaseFormSection label="Name">
      <BaseField label="Name" name="name">
        <BaseInput ref="name" v-model="form.name" name="name" class="w-full" />
      </BaseField>
    </BaseFormSection>

    <div class="flex flex-wrap mt-5">
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
  </BaseForm>
</template>

<script>
import { required } from 'vuelidate/lib/validators'
import Vue from 'vue'
import BaseForm from '@/components/forms/BaseForm.vue'
import BaseFormSection from '@/components/forms/BaseFormSection.vue'
import { objectCompare } from '@/utils/object.js'

export default {
  components: {
    BaseForm,
    BaseFormSection
  },
  props: {
    object: { type: Object, default: null },
    saving: { type: Boolean, default: false },
    saveLabel: { type: String, default: 'Speichern' }
  },
  data() {
    return {
      form: {
        name: ''
      }
    }
  },
  validations() {
    return {
      form: {
        name: { required, unique: this.nameUniqueOrOld }
      }
    }
  },
  computed: {
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
    async nameUniqueOrOld(value) {
      if (!value) {
        return true
      }
      if (this.object && value === this.object.name) {
        return true
      }
      const data = await this.$axios.$get('groups/')
      return data.filter(g => g.name === value).length === 0
    }
  }
}
</script>
