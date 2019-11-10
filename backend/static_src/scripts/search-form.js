document.querySelectorAll('.js-search-form').forEach(function (form) {
  var input = form.querySelector('input');
  var results = form.querySelector('.js-search-form-results');

  input.addEventListener('focus', function (event) {
    results.classList.remove('hidden');
  })

  input.addEventListener('keydown', function (event) {
    if (event.code !== 'ArrowDown') return;
    event.preventDefault();
    results.querySelectorAll('a')[0].focus()
  })
  results.addEventListener('keydown', function (event) {
    if (event.code !== 'ArrowDown') return;
    event.preventDefault();
    var nextSibling = document.activeElement.nextElementSibling;
    if (nextSibling) nextSibling.focus();
  })
  results.addEventListener('keydown', function (event) {
    if (event.code !== 'ArrowUp') return;
    event.preventDefault();
    var prevSibling = document.activeElement.previousElementSibling;
    if (prevSibling) prevSibling.focus();
    else input.focus();

  })

  form.addEventListener('focusout', function (event) {
    if (!form.contains(event.relatedTarget))
      results.classList.add('hidden');
  })

  form.addEventListener('keydown', function (event) {
    if (event.code !== 'Escape') return;
    event.preventDefault();
    input.blur();
    results.classList.add('hidden');
  })

  input.addEventListener('input', function (event) {
    if (input.value.length < 3) {
      results.innerHTML = "";
      return;
    }

    var XHR = new XMLHttpRequest();
    XHR.addEventListener('load', function (loadEvent) {
      if (loadEvent.target.status === 200) {
        results.innerHTML = loadEvent.target.response;
      }
    });
    var target = new URL(form.action);
    target.search = new URLSearchParams({ q: input.value }).toString();
    XHR.open('GET', target);
    XHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    XHR.send();
  });
});