import { helpers } from 'vuelidate/lib/validators'

export function minDate(min) {
  return helpers.withParams(
    { type: 'minDate', min: new Date(min).toLocaleDateString() },
    value => !helpers.req(value) || new Date(value) >= new Date(min)
  )
}

export function checked(value) {
  return !helpers.req(value) || !!value
}
