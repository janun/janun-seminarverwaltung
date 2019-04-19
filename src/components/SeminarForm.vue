<template>
  <b-form @submit.prevent="submit">
    <BFormGroup label="Inhalt">
      <FormInput :validator="$v.form.title" label="Titel" v-model="form.title" />
      <FormTextarea
        :validator="$v.form.description"
        label="Beschreibung"
        v-model="form.description"
      />
    </BFormGroup>

    <BFormGroup label="Zeit &amp; Ort">
      <BFormRow>
        <BCol>
          <FormInput
            type="date"
            :validator="$v.form.start_date"
            label="Start-Datum"
            v-model="form.start_date"
          />
        </BCol>
        <BCol>
          <FormInput
            type="time"
            :validator="$v.form.start_time"
            label="Start-Zeit"
            v-model="form.start_time"
          />
        </BCol>
      </BFormRow>
      <BFormRow>
        <BCol>
          <FormInput
            type="date"
            :validator="$v.form.end_date"
            label="End-Datum"
            v-model="form.end_date"
          />
        </BCol>
        <BCol>
          <FormInput
            type="time"
            :validator="$v.form.end_time"
            label="End-Zeit"
            v-model="form.end_time"
          />
        </BCol>
      </BFormRow>

      <FormInput :validator="$v.form.location" label="Ort" v-model="form.location" />
    </BFormGroup>

    <BFormGroup label="Förderung">
      <FormInput
        :validator="$v.form.planned_training_days"
        label="gepl. Bildungstage"
        v-model="form.planned_training_days"
        type="number"
        min="0"
        step="1"
      />
      <BFormRow>
        <BCol>
          <FormInput
            type="number"
            :validator="$v.form.planned_attendees_min"
            label="gepl. Teilnehmende min."
            v-model="form.planned_attendees_min"
            min="0"
            step="1"
          />
        </BCol>
        <BCol>
          <FormInput
            type="number"
            :validator="$v.form.planned_attendees_max"
            label="gepl. Teilnehmende max."
            v-model="form.planned_attendees_max"
            :min="form.planned_attendees_min"
            step="1"
          />
        </BCol>
      </BFormRow>
      <FormInput
        :validator="$v.form.requested_funding"
        label="Beantragte Förderung in EUR"
        v-model="form.requested_funding"
        type="number"
        min="0"
        step="0.01"
      />
    </BFormGroup>

    <b-button type="submit" :disabled="!hasChanges || $v.form.$invalid || saving" variant="primary">
      <b-spinner small v-if="saving" label="Speichern..." />
      Speichern
    </b-button>
  </b-form>
</template>

<script lang="ts">
import Vue from "vue";
import { Seminar } from "@/types";
import { required } from "vuelidate/lib/validators";

export default Vue.extend({
  props: {
    object: { type: Object as () => Seminar, required: true },
    saving: { type: Boolean, default: false }
  },
  data: () => ({
    form: {
      title: "",
      description: "",
      start_date: "",
      start_time: "",
      end_date: "",
      end_time: "",
      location: "",
      planned_training_days: 0,
      planned_attendees_min: 0,
      planned_attendees_max: 0,
      requested_funding: 0.0
    } as Seminar
  }),
  validations() {
    return {
      form: {
        title: { required },
        description: {},
        start_date: { required },
        start_time: {},
        end_date: { required },
        end_time: {},
        location: { required },
        planned_training_days: { required },
        planned_attendees_min: { required },
        planned_attendees_max: { required },
        requested_funding: {required}
      }
    };
  },
  computed: {
    hasChanges(): boolean {
      if (this.object) {
        for (const key in this.form) {
          if (this.object[key as keyof Seminar] !== this.form[key as keyof Seminar]) {
            return true;
          }
        }
      }
      return false;
    }
  },
  methods: {
    submit() {
      this.$emit("submit", this.form);
    },
    copyFields() {
      if (this.object) {
        for (const key in this.form) {
          if (this.form.hasOwnProperty(key)) {
            Vue.set(this.form, key, this.object[key as keyof Seminar]);
          }
        }
      }
    }
  }
});
</script>
