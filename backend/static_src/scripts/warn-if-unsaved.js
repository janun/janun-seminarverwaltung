/* eslint-disable compat/compat */
document.querySelectorAll('.js-warn-if-unsaved').forEach(function (form) {
  if (!URLSearchParams) return
  var oldData = new URLSearchParams(new FormData(form)).toString()
  var beforeunload = function (event) {
    event.returnValue = 'Es gibt ungespeicherte Änderungen in einem Formular.'
  }

  form.addEventListener('input', function () {
    var newData = new URLSearchParams(new FormData(form)).toString()
    if (oldData !== newData) {
      window.addEventListener('beforeunload', beforeunload)
    } else {
      window.removeEventListener('beforeunload', beforeunload)
    }
  })
})
