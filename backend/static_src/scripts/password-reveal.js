document.querySelectorAll('.js-password-reveal').forEach(function (div) {
  var input = div.querySelector('input');
  var showButton = div.querySelector('.js-show-button');
  var hideButton = div.querySelector('.js-hide-button');

  showButton.addEventListener('click', function (event) {
    input.type = 'text';
    showButton.classList.add('hidden');
    hideButton.classList.remove('hidden');
    input.focus();
  });

  hideButton.addEventListener('click', function (event) {
    input.type = 'password';
    showButton.classList.remove('hidden');
    hideButton.classList.add('hidden');
    input.focus();
  });
});