var elems = document.querySelectorAll('[data-password-toggle]');
for (var i=0; i<elems.length; i++) {
  var button = elems[i];
  button.addEventListener('click', function (event) {
    event.preventDefault();
    var button = event.target;
    var passwordId = button.getAttribute('data-password-toggle');
    var password = document.getElementById(passwordId);
    if (password.type === 'text') {
      password.type = 'password';
      button.text = "anzeigen";
    } else {
      password.type = 'text';
      button.text = "verstecken";
    }
  })
}
