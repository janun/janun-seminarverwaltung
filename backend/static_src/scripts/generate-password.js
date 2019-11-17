function generateRandomByte() {
  var crypto = window.crypto || window.msCrypto;
  if (crypto) {
    return crypto.getRandomValues(new Uint8Array(1))[0];
  }
  return Math.floor(Math.random() * 256);
}

function generatePassword(length) {
  var pattern = /[a-zA-Z0-9_\-+.]/;
  return Array.apply(null, { 'length': length })
    .map(function () {
      var result;
      while (!pattern.test(result)) {
        result = String.fromCharCode(generateRandomByte());
      }
      return result;
    })
    .join('');
}

document.querySelectorAll('.js-generate-password').forEach(function (button) {
  var fieldSelector = button.getAttribute('data-password-field');
  if (!fieldSelector) return;
  var field = document.querySelector(fieldSelector);
  if (!field) return;

  button.addEventListener('click', function (event) {
    event.preventDefault();
    field.value = generatePassword(12);
  })
})