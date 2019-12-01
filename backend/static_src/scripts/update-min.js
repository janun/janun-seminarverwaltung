document.querySelectorAll('.js-update-min').forEach(function (toField) {
  var fromField = document.querySelector(toField.getAttribute('data-min-field'))
  if (!fromField) return

  function updateMin() {
    if (fromField.value)
      toField.setAttribute('min', fromField.value)
  }

  fromField.addEventListener('input', updateMin)
  updateMin()
})