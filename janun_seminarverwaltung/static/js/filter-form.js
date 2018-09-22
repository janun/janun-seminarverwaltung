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
}
