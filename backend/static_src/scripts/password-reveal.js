document.querySelectorAll('.js-password-reveal').forEach(function (div) {
  var input = div.querySelector('input');
  var button = div.querySelector('button');
  var show = button.querySelector('.js-password-reveal-show');
  var hide = button.querySelector('.js-password-reveal-hide');

  button.addEventListener('click', function (event) {
    event.preventDefault();
    if (input.type === 'password') {
      input.type = 'text';
      show.classList.add('hidden');
      hide.classList.remove('hidden');
    } else {
      input.type = 'password'
      show.classList.remove('hidden');
      hide.classList.add('hidden');
    }
  })
})