function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};


// submits the form on change
var filterForms = document.getElementsByClassName('filter-form');
for (var i=0; i<filterForms.length; i++) {
  var form = filterForms[i];

  // submit on select
  var selects = form.querySelectorAll('select');
  for (var j=0; j<selects.length; j++) {
    selects[j].addEventListener('change', function (e) {
      form.submit();
    });
  }

  // reset on ESC
  form.addEventListener('keyup', function (e) {
    if (e.keyCode === 27) {
      window.location = window.location.href.split("?")[0];
    }
  });

  // submit on input text change
  var inputs = form.querySelectorAll('input[type=text]');
  for (var j=0; j<inputs.length; j++) {
    inputs[j].addEventListener('change', function (e) {
      form.submit();
    });
    inputs[j].addEventListener('input',
      debounce(function (e) {form.submit();}, 300)
    );
  }
}
