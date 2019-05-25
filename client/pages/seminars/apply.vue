<template>
  <BaseWizard class="max-w-3xl mx-auto" :title="wizardTitle" @cancel="cancel">
    <BaseWizardStep title="Inhalt" :v="$v.form.content" :prev-disabled="true">
      <h2 class="text-green-500 text-xl mb-4">Seminarinhalte</h2>
      <p class="mb-5">
        Beschreibe uns Dein Seminar, damit wir entscheiden können, ob wir es
        fördern können.
      </p>
      <BaseField label="Titel" name="title">
        <span slot="helptext">
          Beschreibe oder benenne das Seminar in wenigen Worten
        </span>
        <BaseInput v-model="form.content.title" class="w-full" />
      </BaseField>
      <BaseField label="Beschreibung" name="description">
        <span slot="helptext">
          Um was genau geht es in dem Seminar? Welche Inhalte werden vermittelt?
        </span>
        <BaseTextarea
          v-model="form.content.description"
          class="w-full"
          rows="10"
        />
      </BaseField>
    </BaseWizardStep>

    <BaseWizardStep title="Zeit &amp; Ort" :v="$v.form.spacetime">
      <h2 class="text-green-500 text-xl mb-4">Zeit &amp; Ort</h2>
      <div class="flex flex-wrap -mx-2">
        <BaseField label="Start-Datum" class="mx-2" name="start_date">
          <BaseInput
            v-model="form.spacetime.start_date"
            type="date"
            class="max-w-xs"
          />
        </BaseField>
        <BaseField label="Start-Zeit" optional class="mx-2" name="start_time">
          <BaseInput v-model="form.spacetime.start_time" type="time" />
        </BaseField>
      </div>

      <div class="flex flex-wrap -mx-2">
        <BaseField label="End-Datum" class="mx-2" name="end_date">
          <BaseInput
            v-model="form.spacetime.end_date"
            type="date"
            class="max-w-xs"
          />
        </BaseField>
        <BaseField label="End-Zeit" optional class="mx-2" name="end_time">
          <BaseInput v-model="form.spacetime.end_time" type="time" />
        </BaseField>
      </div>

      <BaseField label="Ort" class="max-w-sm" name="location">
        <span slot="helptext">Stadt, in der das Seminar stattfindet.</span>
        <BaseInput v-model="form.spacetime.location" class="w-full" />
      </BaseField>
    </BaseWizardStep>

    <BaseWizardStep title="Gruppe" :v="$v.form.group">
      <h2 class="text-green-500 text-xl mb-4">
        Meldest Du das Seminar für eine Gruppe an?
      </h2>
      <BaseRadioSelect v-model="form.group.yesgroup" :value-if-checked="false">
        Nein, Anmeldung als Einzelperson.
      </BaseRadioSelect>

      <BaseRadioSelect v-model="form.group.yesgroup" :value-if-checked="true">
        Ja, Anmeldung für folgende JANUN-Gruppe:
      </BaseRadioSelect>

      <div v-if="form.group.yesgroup" class="my-4">
        <GroupSelect
          v-if="$auth.user.has_staff_role"
          v-model="form.group.group_pk"
        />
        <p v-else-if="!$auth.user.janun_groups.length">
          Sorry, Du bist in keinen Gruppen eingetragen.
        </p>
        <GroupSelect
          v-else
          v-model="form.group.group_pk"
          :possible-groups="$auth.user.janun_groups"
        />
      </div>
    </BaseWizardStep>

    <BaseWizardStep title="Bildungstage" :v="$v.form.days">
      <h2 class="text-green-500 text-xl mb-4">
        Wieviele Bildungstage hat Dein Seminar?
      </h2>

      <BaseField label="Bildungstage" class="my-4" name="planned_training_days">
        <BaseInput
          v-model="form.days.planned_training_days"
          type="number"
          min="0"
          class="w-32"
        />
      </BaseField>

      <p class="my-6">
        Bildungstage sind Tage, an denen
        <strong>min. 6 Zeitstunden Bildungsarbeit</strong> stattfinden.
      </p>

      <div v-if="isWeekendSeminar !== false">
        <h4 class="font-bold">
          Zweitägige Seminare am Wochenende (Fr/Sa oder Sa/So)
        </h4>
        <p>
          Sind schon 2 Bildungstage, wenn insg. 8 Stunden Bildungsarbeit
          stattfinden.
        </p>
      </div>

      <h4 class="font-bold mt-5">An- und Abreisetage</h4>
      <ul class="list-disc max-w-xl">
        <li class="mb-1">
          Sind zusammen 1 Bildungstag, wenn an beiden zusammen min. 6
          Zeitstunden Bildungsarbeit stattfinden.
        </li>
        <li class="mb-1">
          Sind je 1 Bildungstag, wenn außerdem am Anreisetag vor 12 Uhr begonnen
          wird und am Abreisetag nach 15.30 Uhr geendet wird.
        </li>
      </ul>
    </BaseWizardStep>

    <BaseWizardStep title="Teilnehmende" :v="$v.form.attendees">
      <h2 class="text-green-500 text-xl mb-4">
        Mit wievielen Teilnehmenden rechnest Du?
      </h2>

      <div
        class="text-gray-800 mb-2"
        :class="{ 'text-red-600': $v.form.attendees.$error }"
      >
        geplante Anzahl Teilnehmende
      </div>
      <div class="flex items-start max-w-xs">
        <BaseField
          label="Minimal"
          class="mr-1 flex-1"
          name="planned_attendees_min"
        >
          <BaseInput
            v-model="form.attendees.planned_attendees_min"
            type="number"
            min="0"
            step="1"
          />
        </BaseField>
        <BaseField
          label="Maximal"
          class="ml-1 max-w-xs flex-1"
          name="planned_attendees_max"
        >
          <BaseInput
            v-model="form.attendees.planned_attendees_max"
            type="number"
            :min="form.attendees.planned_attendees_min || 0"
            step="1"
          />
        </BaseField>
      </div>

      <h3 class="font-bold mt-5">Einschränkungen zur Anzahl:</h3>
      <ul class="list-disc max-w-xl">
        <li class=" mb-1">
          Seminare mit weniger als 10 Teilnehmenden können nicht gefördert
          werden.
        </li>
        <li class="mb-1">
          Die Förderung geht nur bis 40 Teilnehmende, aber Ausnahmen sind
          manchmal möglich.
        </li>
      </ul>

      <h3 class="font-bold mt-5">Anforderungen an die Teilnehmenden:</h3>
      <ul class="list-disc max-w-xl">
        <li class=" mb-1">
          Mehr als die Hälfte (50% + 1) der Teilnehmenden müssen ihren Wohnsitz
          in Niedersachsen haben.
        </li>
        <li class="mb-1">
          Mehr als die Hälfte (50% + 1) der Teilnehmenden müssen mindestens 12
          Jahre alt sein und maximal 27.
        </li>
        <p>
          Diese Quoten müssen über den gesamten Seminarzeitraum eingehalten
          werden.
        </p>
      </ul>
    </BaseWizardStep>

    <BaseWizardStep title="Förderung" :v="$v.form.funding">
      <h2 class="text-green-500 text-xl mb-4">
        Wieviel Förderung benötigst Du?
      </h2>
      <p
        v-if="
          $v.form.attendees.$invalid ||
            $v.form.days.$invalid ||
            $v.form.group.$invalid
        "
        class="my-2"
      >
        Bitte fülle vorher die Schritte Gruppe, Bildungstage und Teilnehmende
        aus.
      </p>
      <div v-else>
        <p>
          Aufgrund der eingegeben Daten kannst Du
          <strong>maximal {{ maxFunding | euro }}</strong>
          beantragen. Solltest Du aber auch mit weniger Förderung auskommen,
          können evtl. mehr Seminare bei JANUN stattfinden.
        </p>
        <BaseField
          label="beantragte Förderung in EUR"
          class="my-5"
          name="requested_funding"
          :validator-params="{ maxFunding: formattedMaxFunding }"
        >
          <BaseInput
            v-model="form.funding.requested_funding"
            type="number"
            min="0"
            step="0.01"
            class="w-32"
          />
        </BaseField>
        <p class="text-sm">
          JANUN fördert Seminare, finanziert sie aber nicht komplett. Deswegen
          brauchst Du auch andere Einnahmen (Teilnahmebeiträge, Spenden o.ä.).
          Der Richtwert für Teilnahmebeiträge ist 3,50 € pro Person und Tag.
          Ausgenommen sind eintägige Seminare.
        </p>
      </div>
    </BaseWizardStep>

    <BaseWizardStep
      title="Bestätigung"
      :v="$v.form"
      next-label="Anmelden"
      @submit="save"
    >
      <h2 class="text-green-500 text-xl mb-4">
        Bestätigung
      </h2>

      <div v-if="validExceptConfirmation">
        <BaseCheckbox v-model="form.confirmation.applyFunding" class="my-4">
          Ich möchte die
          <strong
            >Förderung von {{ form.funding.requested_funding | euro }}</strong
          >
          beantragen.
        </BaseCheckbox>

        <BaseCheckbox v-model="form.confirmation.readPolicy" class="my-4">
          Ich habe die
          <a
            href="https://www.janun.de/downloads"
            target="_blank"
            class="font-bold underline"
            >Seminarabrechnungsrichtlinie</a
          >
          gelesen.
        </BaseCheckbox>

        <BaseCheckbox v-model="form.confirmation.acceptDeadline" class="my-4">
          Ich reiche alle Unterlagen bis zur
          <strong>Abrechnungsdeadline am {{ deadline | date }}</strong> ein.
        </BaseCheckbox>
      </div>

      <p v-else>Fülle die vorigen Schritte aus.</p>
    </BaseWizardStep>
  </BaseWizard>
</template>

<script>
import BaseWizard from '@/components/wizard/BaseWizard.vue'
import BaseWizardStep from '@/components/wizard/BaseWizardStep.vue'
import BaseRadioSelect from '@/components/forms/BaseRadioSelect.vue'
import GroupSelect from '@/components/GroupSelect.vue'
import { daysDiff, getDeadline } from '@/utils/date.js'
import { getMaxFunding } from '@/utils/funding.js'
import {
  required,
  minValue,
  maxValue,
  requiredIf
} from 'vuelidate/lib/validators'
import { minDate, checked } from '@/utils/validators.js'
import { formatEuro } from '@/utils/formatters'

export default {
  head() {
    return {
      title: 'Seminar anmelden'
    }
  },
  layout: 'empty',
  components: {
    BaseWizard,
    BaseWizardStep,
    BaseRadioSelect,
    GroupSelect
  },
  data() {
    return {
      modalOpen: false,
      saving: false,
      form: {
        content: {
          title: '',
          description: ''
        },
        spacetime: {
          start_date: '',
          start_time: '',
          end_date: '',
          end_time: '',
          location: ''
        },
        group: {
          group_pk: '',
          yesgroup: null
        },
        days: {
          planned_training_days: null
        },
        attendees: {
          planned_attendees_min: null,
          planned_attendees_max: null
        },
        funding: {
          requested_funding: null
        },
        confirmation: {
          applyFunding: false,
          readPolicy: false,
          acceptDeadline: false
        }
      }
    }
  },
  validations() {
    return {
      form: {
        content: {
          title: { required },
          description: { required }
        },
        spacetime: {
          start_date: { required },
          start_time: {},
          end_date: {
            required,
            minStart: minDate(this.form.spacetime.start_date)
          },
          end_time: {},
          location: { required }
        },
        group: {
          yesgroup: { required },
          group_pk: { require: requiredIf(() => this.form.group.yesgroup) }
        },
        days: {
          planned_training_days: {
            required,
            maxDuration: maxValue(this.duration)
          }
        },
        attendees: {
          planned_attendees_min: { required, minValue: minValue(10) },
          planned_attendees_max: {
            required,
            minPlannedAttendeesMin: minValue(
              this.form.attendees.planned_attendees_min || 0
            )
          }
        },
        funding: {
          requested_funding: { required, maxFunding: maxValue(this.maxFunding) }
        },
        confirmation: {
          applyFunding: { required, checked },
          readPolicy: { required, checked },
          acceptDeadline: { required, checked }
        }
      }
    }
  },
  computed: {
    wizardTitle() {
      const name = this.form.content.title
      if (name) {
        return `${name} anmelden`
      } else {
        return 'Seminar anmelden'
      }
    },
    validExceptConfirmation() {
      if (this.$v.form) {
        const formsExceptConfirmation = Object.keys(this.$v.form)
          .filter(key => !key.startsWith('$'))
          .filter(formName => formName !== 'confirmation')
          .map(formName => this.$v.form[formName])
        return formsExceptConfirmation.every(form => !form.$invalid)
      }
      return false
    },
    deadline() {
      return getDeadline(this.form.spacetime.end_date)
    },
    maxFunding() {
      return getMaxFunding(
        this.form.days.planned_training_days || 0,
        this.form.group.yesgroup || false,
        this.form.attendees.planned_attendees_max || 0
      )
    },
    formattedMaxFunding() {
      return formatEuro(this.maxFunding)
    },
    duration() {
      const start = this.form.spacetime.start_date
      const end = this.form.spacetime.end_date
      if (start && end) {
        return daysDiff(start, end) + 1
      }
      return 0
    },
    isWeekendSeminar() {
      const start = this.form.spacetime.start_date
      const end = this.form.spacetime.end_date
      if (start && end) {
        const startsOnFriOrSat = [5, 6].includes(new Date(start).getDay())
        if (this.duration === 2 && startsOnFriOrSat) {
          return true
        }
        return false
      }
      return undefined
    }
  },
  created() {
    const janunGroups = this.$auth.user.janun_groups
    if (janunGroups.length) {
      this.form.group.yesgroup = true
      this.form.group.group_pk = janunGroups[0].pk
    }
  },
  methods: {
    cancel() {
      this.$router.push('/')
    },
    async save() {
      const payload = {
        title: this.form.content.title,
        description: this.form.content.description,
        start_date: this.form.spacetime.start_date,
        start_time: this.form.spacetime.start_time,
        end_date: this.form.spacetime.end_date,
        end_time: this.form.spacetime.end_time,
        location: this.form.spacetime.location,
        group_pk: this.form.group.yesgroup
          ? this.form.group.group_pk
          : undefined,
        planned_training_days: this.form.days.planned_training_days,
        planned_attendees_min: this.form.attendees.planned_attendees_min,
        planned_attendees_max: this.form.attendees.planned_attendees_max,
        requested_funding: this.form.funding.requested_funding
      }
      this.saving = true
      try {
        const seminar = await this.$axios.$post('seminars/', payload)
        this.modalOpen = true
        this.$router.push(`/seminars/${seminar.pk}`)
      } catch (error) {
        this.$nuxt.error(error)
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
