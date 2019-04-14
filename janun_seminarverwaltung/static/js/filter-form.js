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


// $('.filter-form').each(function () {
// 	var form = $(this);
//
// 	// reset on ESC
// 	$(document).keyup(function(e) {
// 	  if (e.keyCode === 27) {
// 			window.location = window.location.href.split("?")[0];
// 		}
// 	});
//
// 	// submit on input text change
// 	form.find('input[type=text], input[type=number], select').each(function () {
// 		$(this).change(function () { form.submit(); });
// 		// $(this).on('change', debounce(function () {form.submit();}, 1000));
// 	})
// })
