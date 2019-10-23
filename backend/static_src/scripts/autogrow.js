document.querySelectorAll(".js-autogrow").forEach(function (el) {
    el.addEventListener('input', function (event) {
        el.style.setProperty('height', 'auto');
        var newHeight = el.offsetHeight + el.scrollHeight - el.clientHeight;
        el.style.height = newHeight + "px";
    });
});