// .js-is-sticky-b
// detects if element with this class is currently sticky
// and adds/removes the classes from data-sticky-classes attribute
// works for bottom: 0
document.querySelectorAll('.js-is-sticky-b').forEach(function (elem) {
  var classlist = elem.getAttribute('data-sticky-classes').split(' ');

  // fail gracefully
  if (!('IntersectionObserver' in window)) return;

  var observer = new IntersectionObserver(function (entries) {
    if (entries[0].intersectionRatio === 0) {
      classlist.forEach(function (klass) {
        elem.classList.add(klass);
      });
    }
    else if (entries[0].intersectionRatio === 1) {
      classlist.forEach(function (klass) {
        elem.classList.remove(klass);
      });
    }
  }, { threshold: [0, 1] });

  // put sth after elem
  var sentinel = document.createElement('div');
  sentinel.innerHTML = '&nbsp;'
  var style = elem.currentStyle || window.getComputedStyle(elem);
  if (style.marginBottom) {
    sentinel.style.marginTop = "-" + style.marginBottom;
    sentinel.style.marginBottom = style.marginBottom;
  }
  elem.insertAdjacentElement('afterend', sentinel);

  // observe
  observer.observe(sentinel);
})