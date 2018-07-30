// submits the form on change
var filterForms = document.getElementsByClassName('filter-form');
for (var i=0; i<filterForms.length; i++) {
  var form = filterForms[i];
  var inputs = form.querySelectorAll('input, select, textarea');
  for (var j=0; j<inputs.length; j++) {
    inputs[j].addEventListener('change', function (e) {
      form.submit();
    });
  }
}
