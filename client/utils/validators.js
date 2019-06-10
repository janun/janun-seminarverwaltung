import { helpers, minLength } from 'vuelidate/lib/validators'
import { sha1 } from '@/utils/hash.js'
import axios from 'axios'
import { compareTwoStrings } from 'string-similarity'

export function minDate(min) {
  return helpers.withParams(
    { type: 'minDate', min: new Date(min).toLocaleDateString() },
    value => !helpers.req(value) || new Date(value) >= new Date(min)
  )
}

export function notSimiliarTo(similiarTo, degree = 0.6) {
  return helpers.withParams({ type: 'notSimiliarTo', similiarTo }, value => {
    if (
      !helpers.req(value) ||
      !minLength(8)(value) ||
      !helpers.req(similiarTo)
    ) {
      return true
    }
    return [...similiarTo.split(/\W+/), similiarTo].every(
      cmpStr =>
        compareTwoStrings(cmpStr.toLowerCase(), value.toLowerCase()) < degree
    )
  })
}

export function checked(value) {
  return !helpers.req(value) || !!value
}

export async function passwordNotOwned(value) {
  if (!value || !minLength(8)(value)) {
    return true
  }
  const hash = await sha1(value)
  const hashRest = hash.slice(5).toUpperCase()
  try {
    const response = await axios.get(
      `https://api.pwnedpasswords.com/range/${hash.substr(0, 5)}`
    )
    const result = response.data
      .split('\n')
      .find(value => value.substr(0, 35) === hashRest)
    return result == null
  } catch (error) {
    return true
  }
}
