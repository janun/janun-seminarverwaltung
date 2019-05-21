import Vue from 'vue'
import vuelidateErrorExtractor from 'vuelidate-error-extractor'

Vue.use(vuelidateErrorExtractor, {
  messages: {
    required: 'Erforderlich',
    minStart: 'Muss nach Start-Datum liegen.',
    minPlannedAttendeesMin: 'Muss größer sein als der Mindestwert.',
    maxDuration:
      'Darf nicht größer sein als die Dauer des Seminars ({max} Tage).',
    maxFunding: 'Maximal-Förderung: {maxFunding}',
    minFuture: 'Muss in der Zukunft liegen.',
    minLength: 'Mindestens {min} Zeichen',
    email: 'Keine gültige E-Mail-Adresse',
    unique: 'Ist schon vergeben.'
  }
})