import { parseGermanDate, dateIsoString } from "./date-helpers"

document.querySelectorAll('.js-update-min').forEach(function (toField) {
  var fromField = document.querySelector(toField.getAttribute('data-min-field'))
  var isDateField = toField.hasAttribute('data-date-transform')
  if (!fromField) return

  function updateMin() {
    if (fromField.value) {
      var fromValue = fromField.value
      if (isDateField) {
        fromValue = dateIsoString(parseGermanDate(fromValue))
      }
      toField.setAttribute('min', fromValue)
    }
  }

  fromField.addEventListener('input', updateMin)
  updateMin()
})