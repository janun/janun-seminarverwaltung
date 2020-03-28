/* eslint-disable es/no-for-of-loops */

// surround the button with a span
function addButtonContainer(button) {
  var wrapper = document.createElement('span')
  wrapper.setAttribute('title', "Keine Änderungen")
  button.parentNode.insertBefore(wrapper, button)
  wrapper.appendChild(button)
  return wrapper
}

// remove the surrounding span
function removeButtonContainer(button) {
  if (button.parentNode.nodeName === 'SPAN') {
    var span = button.parentNode
    var parent = span.parentNode
    while (span.firstChild) parent.insertBefore(span.firstChild, span);
    parent.removeChild(span);
  }
}

// disable button if no changes in form
// if there are changes, list them in title attribute
document.querySelectorAll('.js-disable-if-unchanged').forEach(function (button) {
  var form = button.form
  var oldData = new FormData(form)
  var oldDataString = new URLSearchParams(oldData).toString()

  function updateState() {
    var newData = new FormData(form)
    var newDataString = new URLSearchParams(newData).toString()

    if (newDataString != oldDataString) {
      button.removeAttribute('disabled')
      removeButtonContainer(button)
    } else {
      button.setAttribute('disabled', true)
      button.removeAttribute('title')
      addButtonContainer(button)
    }
  }

  form.addEventListener('input', updateState)
  updateState()
})