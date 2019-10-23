document.querySelectorAll('.js-focus-invalid').forEach(function (form) {
  var invalidInputs = document.querySelectorAll('.is-invalid')
  if (invalidInputs.length > 0) {
    setTimeout(function () {
      invalidInputs[0].focus();
    }, 10);
  }
})