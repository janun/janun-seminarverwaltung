// .js-is-sticky-b
// detects if element with this class is currently sticky
// and adds/removes the classes from data-sticky-classes attribute
// works for bottom: 0
document.querySelectorAll('.js-is-sticky-b').forEach(function (elem) {
    classlist = elem.getAttribute('data-sticky-classes').split(' ');

    function detectSticky() {
        if (window.innerHeight - elem.getBoundingClientRect().bottom <= 0) {
            classlist.forEach(function (klass) {
                elem.classList.add(klass);
            });
        } else {
            classlist.forEach(function (klass) {
                elem.classList.remove(klass);
            });
        }
    }

    document.addEventListener('scroll', detectSticky);
    detectSticky();
})