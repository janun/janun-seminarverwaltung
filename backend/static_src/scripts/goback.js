document.querySelectorAll(".js-goback").forEach(function (elem) {
  elem.addEventListener('click', function (event) {
    event.preventDefault();
    window.history.back();
  });
})