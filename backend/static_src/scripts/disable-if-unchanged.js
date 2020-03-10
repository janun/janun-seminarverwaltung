/* eslint-disable es/no-for-of-loops */
// get changed fields between two FormData objects
// doesnt work in ie
function getChangedFields(oldData, newData) {
  var fields = []
  var oldKeys = Array.from(oldData.keys())
  var newKeys = Array.from(newData.keys())

  for (var key of oldKeys) {
    var oldValue = oldData.get(key)
    var newValue = newData.get(key)

    // field was removed
    if (!newKeys.includes(key)) {
      fields.push(key)
    }

    // compare uploads by size
    if (oldValue instanceof File) {
      if (oldValue.size != newValue.size) fields.push(key)
    }
    else if (oldValue !== newValue) fields.push(key)
  }

  // check for added keys
  for (var key2 of newKeys) {
    if (!oldKeys.includes(key2)) {
      fields.push(key2)
    }
  }

  return fields
}

function getLabel(form, fieldName) {
  var field = form.querySelector('[name="' + fieldName + '"]')
  return field.labels[0].innerText
}

// surround the button with a span
function addButtonContainer(button) {
  var wrapper = document.createElement('span')
  wrapper.setAttribute('title', "Keine Änderungen")
  button.parentNode.insertBefore(wrapper, button)
  wrapper.appendChild(button)
  return wrapper
}

// remove the surrounding span
function removeButtonContainer(button) {
  if (button.parentNode.nodeName === 'SPAN') {
    var span = button.parentNode
    var parent = span.parentNode
    while (span.firstChild) parent.insertBefore(span.firstChild, span);
    parent.removeChild(span);
  }
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
      removeButtonContainer(button)
      var labels = changedFields.map(function (field) { return getLabel(form, field) })
      var title = "Änderungen an " + labels.join(', ') + " speichern."
      button.setAttribute('title', title)
    } else {
      button.setAttribute('disabled', true)
      button.removeAttribute('title')
      addButtonContainer(button)
    }
  }

  form.addEventListener('input', updateState)
  updateState()
})