document.querySelectorAll('.js-row-link').forEach(function (container) {

  container.querySelectorAll("[data-link]").forEach(function (row) {
    var href = row.getAttribute('data-link')
    var firstCol = row.querySelector('td');
    var newLink = document.createElement("a");
    newLink.setAttribute('href', href)
    firstCol.appendChild(newLink);
    firstCol.style.position = 'relative';
    newLink.style.cssText = "position: absolute; display: block; top: 0; left: 0; z-index: 0; height: 100%;"

    function setWidth(event) {
      newLink.style.width = row.clientWidth + 'px';
    }
    window.addEventListener('resize', setWidth, { passive: true });
    setWidth();
  })
})