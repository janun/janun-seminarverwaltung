var invalidField = document.querySelector('.js-focus-invalid .is-invalid');
if (invalidField) {
  // setTimeout to work around autofocus on other form fields
  setTimeout(function () {
    invalidField.focus();
  }, 10);
}