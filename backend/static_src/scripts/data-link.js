document.querySelectorAll('.js-data-link').forEach(function (container) {
  container.querySelectorAll("[data-link]").forEach(function (link) {
    var href = link.getAttribute('data-link')
    link.addEventListener('click', function (event) {
      if (!window.getSelection().toString()) {
        window.location.href = href;
      }
    })
  })
})