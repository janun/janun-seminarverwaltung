document.querySelectorAll('.js-search-form').forEach(function (form) {
  var input = form.querySelector('input');
  var results = form.querySelector('.js-search-form-results');

  // focus on Ctrl+Shift+F
  document.addEventListener('keydown', function (event) {
    if (event.ctrlKey && event.shiftKey && event.key.toLowerCase() === 'f') {
      input.focus();
    }
  })

  // show results when focus
  input.addEventListener('focus', function () {
    results.classList.remove('hidden');
  })

  // select first result on ArrowDown
  input.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowDown' || event.key == 'Down') {
      event.preventDefault();
      results.querySelectorAll('a')[0].focus()
    }
  })

  // cycle results and inputs on ArrowDown / ArrowUp
  results.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowDown' || event.key == 'Down') {
      event.preventDefault();
      var nextSibling = document.activeElement.nextElementSibling;
      if (nextSibling) nextSibling.focus();
    }
  })
  results.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowUp' || event.key == 'Up') {
      event.preventDefault();
      var prevSibling = document.activeElement.previousElementSibling;
      if (prevSibling) prevSibling.focus();
      else input.focus();
    }
  })

  // hide results on focusout or Escape
  form.addEventListener('focusout', function (event) {
    if (!form.contains(event.relatedTarget))
      results.classList.add('hidden');
  })
  form.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' || event.key === 'Esc') {
      event.preventDefault();
      input.blur();
      results.classList.add('hidden');
    }
  })

  // start the search on input
  input.addEventListener('input', function () {
    if (input.value.length === 0) {
      results.innerHTML = "";
      return;
    }

    var XHR = new XMLHttpRequest();
    XHR.addEventListener('load', function (loadEvent) {
      if (loadEvent.target.status === 200) {
        results.innerHTML = loadEvent.target.response;
      }
    });
    XHR.open('GET', form.action + "?q=" + encodeURIComponent(input.value));
    XHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    XHR.send();
  });
});