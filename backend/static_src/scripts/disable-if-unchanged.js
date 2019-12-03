/* eslint-disable es/no-for-of-loops */
// get changed fields between two FormData objects
// doesnt work in ie
function getChangedFields(oldData, newData) {
  var fields = []
  for (var key of oldData.keys()) {
    if (oldData.get(key) !== newData.get(key)) fields.push(key)
  }
  return fields
}

function getLabel(form, fieldName) {
  var field = form.querySelector('[name="' + fieldName + '"]')
  return field.labels[0].innerText
}

// disable button if no changes in form
// if there are changes, list them in title attribute
document.querySelectorAll('.js-disable-if-unchanged').forEach(function (button) {
  var form = button.form
  var oldData = new FormData(form)

  function updateState() {
    var newData = new FormData(form)
    var changedFields = getChangedFields(oldData, newData)

    if (changedFields.length > 0) {
      button.removeAttribute('disabled')
      var labels = changedFields.map(function (field) { return getLabel(form, field) })
      var title = "Änderungen an " + labels.join(', ') + " speichern."
      button.setAttribute('title', title)
    } else {
      button.setAttribute('disabled', true)
    }
  }

  form.addEventListener('input', updateState)
  updateState()
})