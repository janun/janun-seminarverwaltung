var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();

// submits the form on change
var filterForms = document.getElementsByClassName('filter-form');
for (var i=0; i<filterForms.length; i++) {
  var form = filterForms[i];

  var selects = form.querySelectorAll('select');
  for (var j=0; j<selects.length; j++) {
    selects[j].addEventListener('change', function (e) {
      form.submit();
    });
  }

  var inputs = form.querySelectorAll('input, textarea');
  for (var k=0; k<inputs.length; k++) {
    inputs[k].addEventListener('input', function (e) {
      delay(function () { form.submit() }, 500);
    });
  }
}
