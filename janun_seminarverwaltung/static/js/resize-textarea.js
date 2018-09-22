var textareas = document.querySelectorAll('textarea');
for (var i=0; i < textareas.length; i++) {
  textareas[i].style.resize = "none";
  textareas[i].style.overflow = "hidden";
  textareas[i].addEventListener('input', function (event) {
    var el = event.target;
    el.style.height = 'auto';
    el.style.height = el.scrollHeight + 'px';
  });
}
