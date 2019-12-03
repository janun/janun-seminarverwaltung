// adds class 'submit-attempted' to all form, when submit button is clicked
// can be used to unhide client validation messages
document.querySelectorAll('form').forEach(function (form) {
  var submitButton = form.querySelector('button[type=submit]')
  if (!submitButton) return

  submitButton.addEventListener('click', function () {
    form.classList.add('submit-attempted')
  })

})