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
      label.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon-view-visible"><path class="primary" d="M17.56 17.66a8 8 0 0 1-11.32 0L1.3 12.7a1 1 0 0 1 0-1.42l4.95-4.95a8 8 0 0 1 11.32 0l4.95 4.95a1 1 0 0 1 0 1.42l-4.95 4.95zM11.9 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10z"/><circle cx="12" cy="12" r="3" class="secondary"/></svg>';
    } else {
      password.type = 'text';
      label.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon-view-hidden"><path class="primary" d="M15.1 19.34a8 8 0 0 1-8.86-1.68L1.3 12.7a1 1 0 0 1 0-1.42l2.88-2.88 2.8 2.8a5 5 0 0 0 5.73 5.73l2.4 2.4zM8.84 4.6a8 8 0 0 1 8.7 1.74l4.96 4.95a1 1 0 0 1 0 1.42l-2.78 2.78-2.87-2.87a5 5 0 0 0-5.58-5.58L8.85 4.6z"/><path class="secondary" d="M3.3 4.7l16 16a1 1 0 0 0 1.4-1.4l-16-16a1 1 0 0 0-1.4 1.4z"/></svg>';
    }
    password.focus();
  })
}
