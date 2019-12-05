import { parseGermanDate } from "./date-helpers"

// sets max attribute according to days between start_date and end_date in same form
document.querySelectorAll('.js-update-max-from-date-diff').forEach(function (toField) {
  var form = toField.form
  var startField = form.querySelector('#id_start_date')
  var endField = form.querySelector('#id_end_date')

  if (!startField || !endField) return

  function update() {
    var start = parseGermanDate(startField.value)
    var end = parseGermanDate(endField.value)

    if (start && end) {
      var diffTime = Math.abs(end - start);
      var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      toField.setAttribute('max', diffDays + 1)
    } else {
      toField.removeAttribute('max')
    }
  }

  startField.addEventListener('input', update)
  endField.addEventListener('input', update)
  update()
})