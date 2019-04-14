function registerDataLinks() {
  var links = document.querySelectorAll('[data-link]');
  for (var i=0; i<links.length; i++) {
    var linkEl = links[i];
    linkEl.addEventListener('click', function(event) {
      var el = event.target;
      while (el.parentNode) {
          el = el.parentNode;
          var href = el.getAttribute('data-link');
          if (href) {
            window.location = href;
            return null;
          }
      }
      return null;
    });
  }
}
registerDataLinks();
