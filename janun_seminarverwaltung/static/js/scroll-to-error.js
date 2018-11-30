var errorElems = document.getElementsByClassName('is-invalid')
if (errorElems.length > 0) {
  errorElems[0].scrollIntoView({'inline': 'center'});
  errorElems[0].focus();
}
