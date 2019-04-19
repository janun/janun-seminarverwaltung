<template>
  <form @submit.prevent="save">
    <div class="columns">
      <div class="column is-one-quarter"><h2 class="label">Inhalt</h2></div>
      <div class="column">
        <FormInput label="Titel" v-model="form.title" :validator="$v.form.title" />
        <FormGroup :validator="$v.form.description" label="Beschreibung">
          <b-input
            type="textarea"
            v-model="form.description"
            @input="$v.form.description.$touch()"
          />
        </FormGroup>
      </div>
    </div>

    <hr />

    <div class="columns">
      <div class="column is-one-quarter"><h2 class="label">Zeit &amp; Ort</h2></div>
      <div class="column">
        <b-field grouped>
          <FormInput
            type="date"
            label="Start-Datum"
            v-model="form.start_date"
            :validator="$v.form.start_date"
          />
          <FormInput
            type="time"
            label="Start-Zeit"
            v-model="form.start_time"
            :validator="$v.form.start_time"
          />
        </b-field>
        <b-field grouped>
          <FormInput
            type="date"
            label="End-Datum"
            v-model="form.end_date"
            :validator="$v.form.end_date"
          />
          <FormInput
            type="time"
            label="End-Zeit"
            v-model="form.end_time"
            :validator="$v.form.end_time"
          />
        </b-field>

        <FormInput label="Ort" v-model="form.location" :validator="$v.form.location" />
      </div>
    </div>

    <hr />

    <div class="columns">
      <div class="column is-one-quarter"><h2 class="label">Förderung</h2></div>
      <div class="column">
        <FormInput
          label="geplante Bildungstage"
          type="number"
          min="0"
          step="1"
          v-model="form.planned_training_days"
          :validator="$v.form.planned_training_days"
        />

        <fieldset>
          <span class="label">geplante Anzahl Teilnehmende</span>
          <b-field grouped>
            <FormInput
              type="number"
              message="minimal"
              min="0"
              step="1"
              v-model="form.planned_attendees_min"
              :validator="$v.form.planned_attendees_min"
            />
            <FormInput
              type="number"
              message="maximal"
              :min="form.planned_attendees_min"
              step="1"
              v-model="form.planned_attendees_max"
              :validator="$v.form.planned_attendees_max"
            />
          </b-field>
        </fieldset>

        <FormInput
          label="beantragte Förderung in €"
          type="number"
          min="0"
          step="0.01"
          v-model="form.requested_funding"
          :validator="$v.form.requested_funding"
        />
      </div>
    </div>

    <hr />

    <b-button
      class="is-pulled-right"
      native-type="submit"
      :disabled="!hasChanges || $v.form.$invalid || saving"
      type="is-primary"
      :loading="saving"
    >
      Speichern
    </b-button>
  </form>
</template>

<script lang="ts">
import Vue from "vue";
import { Seminar } from "@/types";
import { required } from "vuelidate/lib/validators";

export default Vue.extend({
  props: {
    object: { type: Object as () => Seminar, required: true }
  },
  data: () => ({
    saving: false,
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
        requested_funding: { required }
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
    async save() {
      this.saving = true;
      try {
        await this.$store.dispatch("seminars/update", {
          pk: this.object.pk,
          data: this.form
        });
        this.copyFields();
        this.$snackbar.open(`Seminar gespeichert.`);
      } catch (error) {
        this.$snackbar.open({ message: `Fehler beim speichern des Seminars`, type: "is-warning" });
      }
      this.saving = false;
    },
    copyFields() {
      this.$v.$reset();
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
