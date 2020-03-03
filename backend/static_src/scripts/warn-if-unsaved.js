/* eslint-disable compat/compat */
// displays a warning dialog if the user leaves the page when there are unsaved changes
document.querySelectorAll('.js-warn-if-unsaved').forEach(function (form) {
  if (!URLSearchParams) return
  var submitted = false
  var initialData = new URLSearchParams(new FormData(form)).toString()

  var beforeunload = function (event) {
    if (submitted) return
    var currentData = new URLSearchParams(new FormData(form)).toString()
    if (initialData !== currentData) {
      event.preventDefault();
      event.returnValue = 'Es gibt ungespeicherte Änderungen.'
    }
  }
  window.addEventListener('beforeunload', beforeunload)

  form.addEventListener('submit', function () {
    submitted = true
  })
})
