// containers with a class of 'js-sum' will get all their inputs summed on input
// and the result saved in the first element with a class of js-sum-result
function updateTotal(fromFields, toField) {
  var sum = 0.0;
  for (var i = 0; i < fromFields.length; i++) {
    var value = parseFloat(fromFields[i].value.replace(',', '.'));
    if (!isNaN(value)) {
      sum += value;
    }
  }
  toField.innerHTML = sum.toLocaleString("de", { style: "currency", currency: "EUR" })
}

document.querySelectorAll(".js-sum").forEach(function (fieldset) {
  var inputs = fieldset.querySelectorAll('input')
  var output = fieldset.querySelector('.js-sum-result')
  inputs.forEach(function (input) {
    input.addEventListener("input", function () {
      updateTotal(inputs, output)
    });
  })
  updateTotal(inputs, output);
})