<template>
  <form @submit.prevent="save">
    <div class="clearfix mt-5">
      <div class="float-right">
        <button
          class="btn btn-primary mb-1 float-right"
          :class="{ 'btn-loading': saving }"
          type="submit"
          :disabled="$v.form.$invalid || saving || !hasChanges"
        >
          Speichern
        </button>
        <p v-if="$v.form.$error" class="text-red-600">Fehler im Formular</p>
      </div>
    </div>

    <hr class="bg-gray-300 h-px my-5" />

    <BaseFormSection label="Status">
      <SeminarStatus
        v-model="form.status"
        :seminar="seminar"
        class="inline-block"
      />
    </BaseFormSection>

    <BaseFormSection label="Inhalt">
      <BaseField label="Titel" :validator="$v.form.title">
        <BaseInput v-model="form.title" class="w-full" />
      </BaseField>

      <BaseField label="Beschreibung" :validator="$v.form.description">
        <BaseTextarea v-model="form.description" class="w-full" />
      </BaseField>
    </BaseFormSection>

    <BaseFormSection label="Zeit &amp; Ort">
      <div class="flex flex-wrap -mx-2">
        <BaseField
          label="Start-Datum"
          class="mx-2"
          :validator="$v.form.start_date"
        >
          <BaseInput v-model="form.start_date" type="date" class="max-w-xs" />
        </BaseField>
        <BaseField
          label="Start-Zeit"
          class="mx-2"
          :validator="$v.form.start_time"
        >
          <BaseInput v-model="form.start_time" type="time" />
        </BaseField>
      </div>

      <div class="flex flex-wrap -mx-2">
        <BaseField label="End-Datum" class="mx-2" :validator="$v.form.end_date">
          <BaseInput v-model="form.end_date" type="date" class="max-w-xs" />
        </BaseField>
        <BaseField label="End-Zeit" class="mx-2" :validator="$v.form.end_time">
          <BaseInput v-model="form.end_time" type="time" />
        </BaseField>
      </div>

      <BaseField label="Ort" class="max-w-sm" :validator="$v.form.location">
        <span slot="helptext">Stadt, in der das Seminar stattfindet.</span>
        <BaseInput v-model="form.location" class="w-full" />
      </BaseField>
    </BaseFormSection>

    <BaseFormSection label="Förderung">
      <div slot="description" class="mt-3">
        Mögliche Förderung: {{ maxFunding | euro }}
      </div>

      <BaseField label="Gruppe" class="max-w-xs">
        <GroupSelect v-if="$auth.user.has_staff_role" v-model="form.group_pk" />
        <BaseInput
          v-else
          readonly
          :value="seminar.group ? seminar.group.name : '- keine -'"
          class="w-full"
          title="nicht editierbar"
        />
      </BaseField>

      <BaseField
        label="geplante Bildungstage"
        :validator="$v.form.planned_training_days"
      >
        <BaseInput
          v-model="form.planned_training_days"
          type="number"
          min="0"
          :max="duration"
          step="1"
          class="w-full max-w-xxs"
        />
      </BaseField>

      <BaseField label="geplante Anzahl Teilnehmende">
        <div class="flex items-start max-w-xs">
          <BaseField
            label=""
            class="mr-1 flex-1"
            :validator="$v.form.planned_attendees_min"
          >
            <BaseInput
              v-model="form.planned_attendees_min"
              type="number"
              min="0"
              step="1"
              class="w-full"
            />
          </BaseField>
          <span class="mt-3 mx-2">bis</span>
          <BaseField
            label=""
            class="ml-1 max-w-xs flex-1"
            :validator="$v.form.planned_attendees_max"
          >
            <BaseInput
              v-model="form.planned_attendees_max"
              type="number"
              :min="form.planned_attendees_min || 0"
              step="1"
              class="w-full"
            />
          </BaseField>
        </div>
      </BaseField>

      <BaseField
        label="beantragte Förderung in EUR"
        class="max-w-xs"
        :validator="$v.form.requested_funding"
        :validator-params="{ maxFunding: formattedMaxFunding }"
      >
        <BaseInput
          v-model="form.requested_funding"
          type="number"
          min="0"
          step="0.01"
          class="w-full"
        />
      </BaseField>
    </BaseFormSection>

    <hr class="bg-gray-300 h-px my-5 mt-20" />

    <div class="clearfix">
      <div class="float-right mb-16">
        <button
          class="btn btn-primary float-right mb-2"
          :class="{ 'btn-loading': saving }"
          type="submit"
          :disabled="$v.form.$invalid || saving || !hasChanges"
        >
          Speichern
        </button>
        <p v-if="$v.form.$error" class="text-red-600">Fehler im Formular</p>
      </div>
    </div>
  </form>
</template>

<script>
import Vue from 'vue'

import { required, minValue, maxValue } from 'vuelidate/lib/validators'
import { minDate } from '@/utils/validators.js'
import { daysDiff } from '@/utils/date.js'
import { getMaxFunding } from '@/utils/funding.js'
import SeminarStatus from '@/components/SeminarStatus.vue'
import GroupSelect from '@/components/GroupSelect.vue'
import { formatEuro } from '../utils/formatters'
import { objectCompare } from '@/utils/object.js'

export default {
  components: {
    SeminarStatus,
    GroupSelect
  },
  props: {
    seminar: { type: Object, required: true },
    saving: { type: Boolean, default: false }
  },
  data: () => ({
    form: {
      status: '',
      title: '',
      description: '',
      start_date: '',
      start_time: '',
      end_date: '',
      end_time: '',
      location: '',
      group_pk: '',
      planned_training_days: 0,
      planned_attendees_min: 0,
      planned_attendees_max: 0,
      requested_funding: 0.0
    }
  }),
  validations() {
    return {
      form: {
        title: { required },
        description: {},
        start_date: { required },
        start_time: {},
        end_date: { required, minStart: minDate(this.form.start_date) },
        end_time: {},
        location: { required },
        group_pk: {},
        planned_training_days: {
          required,
          maxDuration: maxValue(this.duration)
        },
        planned_attendees_min: { required },
        planned_attendees_max: {
          required,
          minPlannedAttendeesMin: minValue(this.form.planned_attendees_min)
        },
        requested_funding: { required, maxFunding: maxValue(this.maxFunding) }
      }
    }
  },
  computed: {
    hasChanges() {
      return Object.keys(this.form).some(
        key => !objectCompare(this.form[key], this.seminar[key])
      )
    },
    maxFunding() {
      return getMaxFunding(
        this.form.planned_training_days,
        !!this.seminar.group,
        this.form.planned_attendees_max
      )
    },
    formattedMaxFunding() {
      return formatEuro(this.maxFunding)
    },
    duration() {
      if (this.form.start_date && this.form.end_date) {
        return (
          daysDiff(
            new Date(this.form.start_date),
            new Date(this.form.end_date)
          ) + 1
        )
      }
      return 0
    }
  },
  created() {
    this.copyFields()
    this.$v.form.$touch()
  },
  methods: {
    copyFields() {
      this.$v.$reset()
      Object.keys(this.form).forEach(key =>
        Vue.set(this.form, key, this.seminar[key])
      )
    },
    save() {
      this.$emit('save', this.form)
    }
  }
}
</script>
