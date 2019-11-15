document.querySelectorAll('.js-row-link').forEach(function (container) {

  var links = [];

  // insert a.js-row-link-link in first td
  container.querySelectorAll("[data-link]").forEach(function (row) {
    var href = row.getAttribute('data-link');
    var firstCol = row.querySelector('td');
    var newLink = document.createElement("a");
    newLink.setAttribute('href', href)
    newLink.classList.add('js-row-link-link');
    firstCol.insertBefore(newLink, firstCol.firstChild);
    links.push(newLink);
  })

  var style = document.createElement('style');
  container.appendChild(style);

  // set width of those as
  function setWidths(event) {
    var width = container.clientWidth + 'px';
    style.innerHTML = ".js-row-link-link.js-row-link-link { width: " + width + " }"
  }

  // debounced resize
  var resizeTimer = false;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(setWidths, 100);
  });

  setWidths();
})