var elems = document.querySelectorAll('[data-password-toggle]');
for (var i=0; i<elems.length; i++) {
  var checkbox = elems[i];
  checkbox.addEventListener('change', function (event) {
    event.preventDefault();
    var checkbox = event.target;
    var passwordId = checkbox.getAttribute('data-password-toggle');
    var label = document.getElementById(passwordId + '-togglelabel');
    var password = document.getElementById(passwordId);
    if (password.type === 'text') {
      password.type = 'password';
      label.textContent = "anzeigen";
    } else {
      password.type = 'text';
      label.textContent = "verstecken";
    }
    password.focus();
  })
}
