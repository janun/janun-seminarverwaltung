function moveCursorToEnd(el) {
    var index=el.value.length;
    el.setSelectionRange(index,index);
}

var autofocusEls = document.querySelectorAll('.filter-form input[autofocus]');
for (var i=0; i < autofocusEls.length; i++) {
  autofocusEls[i].addEventListener('focus', function (event) {
    moveCursorToEnd(event.target)
  });
  moveCursorToEnd(autofocusEls[i]);
}
