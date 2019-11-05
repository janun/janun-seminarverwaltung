document.querySelectorAll('.js-scroll-spy').forEach(function (container) {
  var sectionOffsets = {}
  container.querySelectorAll('.js-scroll-spy-section').forEach(function (section) {
    sectionOffsets[section.id] = section.offsetTop;
  })

  var menu = container.querySelector('.js-scroll-spy-menu');
  var activeClass = 'js-scroll-spy-active';
  var activeClasses = menu.getAttribute('data-js-scroll-spy-class').split(' ');
  var offset = menu.getAttribute('data-offset');

  function onScroll(event) {
    var scrollPosition = document.documentElement.scrollTop || document.body.scrollTop;
    scrollPosition = parseInt(scrollPosition);
    if (offset) {
      scrollPosition -= offset;
    }

    for (i in sectionOffsets) {
      if (sectionOffsets[i] <= scrollPosition) {
        var oldActive = menu.querySelector('.' + activeClass)
        if (oldActive) {
          oldActive.classList.remove(activeClass);
          activeClasses.forEach(function (klass) {
            oldActive.classList.remove(klass);
          });
        }
        var newActive = menu.querySelector('a[href*=' + i + ']');
        if (newActive) {
          newActive.classList.add(activeClass);
          activeClasses.forEach(function (klass) {
            newActive.classList.add(klass);
          });
        }
      }
    }
  }

  document.addEventListener('scroll', onScroll);
  onScroll();
})