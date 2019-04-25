import { helpers } from 'vuelidate/lib/validators';

export function minDate(min: string | Date) {
  return helpers.withParams(
    { type: 'minDate', min: new Date(min).toLocaleDateString() },
    (value) => !helpers.req(value) || new Date(value) >= new Date(min)
  );
}

export function checked(value: any) {
  return !helpers.req(value) || !!value;
}
