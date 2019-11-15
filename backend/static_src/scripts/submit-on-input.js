document.querySelectorAll('.js-submit-on-input').forEach(function (form) {
  form.querySelectorAll('select').forEach(function (input) {
    input.addEventListener('change', function (event) {
      form.submit();
    })
  })
})