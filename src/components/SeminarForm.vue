<template>
  <form @submit.prevent="save">
    <div class="clearfix mt-5">
      <div class="float-right">
        <button
          class="btn btn-primary mb-1 float-right"
          :class="{ 'btn-loading': saving }"
          type="submit"
          :disabled="$v.form.$invalid || saving"
        >
          Speichern
        </button>
        <p v-if="$v.form.$error" class="text-red-600">Fehler im Formular</p>
      </div>
    </div>

    <hr class="bg-gray-300 h-px my-5" />

    <div class="flex flex-wrap">
      <h2 class="w-full md:w-1/3 text-green-500 mb-5 font-bold">Status</h2>

      <div class="w-full md:w-2/3">
        <SeminarStatus v-model="form.status" :seminar="object" class="inline-block" />
      </div>
    </div>

    <hr class="bg-gray-300 h-px my-5" />

    <div class="flex flex-wrap">
      <h2 class="w-full md:w-1/3 text-green-500 mb-5 font-bold">Inhalt</h2>

      <div class="w-full md:w-2/3">
        <BaseField label="Titel" :validator="$v.form.title">
          <BaseInput v-model="form.title" class="w-full" />
        </BaseField>

        <BaseField label="Beschreibung" :validator="$v.form.description">
          <BaseTextarea v-model="form.description" class="w-full" />
        </BaseField>
      </div>
    </div>

    <hr class="bg-gray-300 h-px my-5" />

    <div class="flex flex-wrap">
      <h2 class="w-full md:w-1/3 text-green-500 mb-5 font-bold">Zeit &amp; Ort</h2>

      <div class="w-full md:w-2/3">
        <div class="flex flex-wrap -mx-2">
          <BaseField label="Start-Datum" class="mx-2" :validator="$v.form.start_date">
            <BaseInput v-model="form.start_date" type="date" class="max-w-xs" />
          </BaseField>
          <BaseField label="Start-Zeit" class="mx-2" :validator="$v.form.start_time">
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
      </div>
    </div>

    <hr class="bg-gray-300 h-px my-5" />

    <div class="flex flex-wrap">
      <div class="w-full md:w-1/3 mb-5">
        <h2 class="text-green-500 font-bold">Förderung</h2>
        <div class="my-3">Mögliche Förderung: {{ maxFunding | euro }}</div>
      </div>

      <div class="w-full md:w-2/3">
        <BaseField label="Gruppe" class="max-w-xs">
          <GroupSelect v-if="isStaff" v-model="form.group_pk" />
          <BaseInput
            v-else
            readonly
            :value="object.group ? object.group.name : '- keine -'"
            class="w-full"
            title="nicht editierbar"
          />
        </BaseField>

        <BaseField label="geplante Bildungstage" :validator="$v.form.planned_training_days">
          <BaseInput
            v-model="form.planned_training_days"
            type="number"
            min="0"
            :max="duration"
            step="1"
            class="w-full max-w-xxs"
          />
        </BaseField>

        <div
          class="text-gray-700"
          :class="{
            'text-red-600':
              $v.form.planned_attendees_min.$error || $v.form.planned_attendees_max.$error
          }"
        >
          geplante Anzahl Teilnehmende
        </div>
        <div class="flex items-start max-w-xs">
          <BaseField label="" class="mr-1 flex-1" :validator="$v.form.planned_attendees_min">
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
      </div>
    </div>

    <hr class="bg-gray-300 h-px my-5 mt-20" />

    <div class="clearfix">
      <div class="float-right mb-16">
        <button
          class="btn btn-primary float-right mb-2"
          :class="{ 'btn-loading': saving }"
          type="submit"
          :disabled="$v.form.$invalid || saving"
        >
          Speichern
        </button>
        <p v-if="$v.form.$error" class="text-red-600">Fehler im Formular</p>
      </div>
    </div>
  </form>
</template>

<script lang="ts">
import Vue from 'vue';
import { Seminar } from '@/types';
import { required, minValue, maxValue } from 'vuelidate/lib/validators';
import { minDate } from '@/utils/validators.ts';
import { daysDiff } from '@/utils/date.ts';
import { getMaxFunding } from '@/utils/funding.ts';
import BaseInput from '@/components/BaseInput.vue';
import BaseTextarea from '@/components/BaseTextarea.vue';
import BaseField from '@/components/BaseField.vue';
import SeminarStatus from '@/components/SeminarStatus.vue';
import GroupSelect from '@/components/GroupSelect.vue';
import { RuleDecl } from 'vue/types/options';
import { formatEuro } from '../utils/formatters';
import userMixin from '@/mixins/user.ts';

export default Vue.extend({
  components: {
    BaseInput,
    BaseField,
    BaseTextarea,
    SeminarStatus,
    GroupSelect
  },
  mixins: [userMixin],
  props: {
    object: { type: Object as () => Seminar, required: true }
  },
  data: () => ({
    saving: false,
    form: {
      status: '' as any,
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
    } as Seminar
  }),
  validations(): RuleDecl {
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
        planned_training_days: { required, maxDuration: maxValue(this.duration) },
        planned_attendees_min: { required },
        planned_attendees_max: {
          required,
          minPlannedAttendeesMin: minValue(this.form.planned_attendees_min)
        },
        requested_funding: { required, maxFunding: maxValue(this.maxFunding) }
      }
    };
  },
  computed: {
    maxFunding(): number {
      return getMaxFunding(
        this.form.planned_training_days,
        !!this.object.group,
        this.form.planned_attendees_max
      );
    },
    formattedMaxFunding(): string {
      return formatEuro(this.maxFunding);
    },
    duration(): number {
      if (this.form.start_date && this.form.end_date) {
        return daysDiff(new Date(this.form.start_date), new Date(this.form.end_date)) + 1;
      }
      return 0;
    }
  },
  created() {
    this.copyFields();
    (this.$v.form as any).$touch();
  },
  methods: {
    async save() {
      this.saving = true;
      try {
        await this.$store.dispatch('seminars/update', {
          pk: this.object.pk,
          data: this.form
        });
        this.copyFields();
        this.$toast(`Seminar gespeichert.`);
      } catch (error) {
        this.$toast(`Fehler beim Speichern des Seminars.`, { type: 'error' }); // TODO: Infobox Erklärung des Fehlers
      }
      this.saving = false;
    }
  }
});
</script>
