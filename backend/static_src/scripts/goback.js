document.querySelectorAll(".js-goback").forEach(function (link) {
  link.addEventListener('click', function (event) {
    event.preventDefault();
    window.history.back();
  });
});