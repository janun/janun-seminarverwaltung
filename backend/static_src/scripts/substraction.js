function parseNumber(string) {
  string = string.replace('.', '').replace(',', '.')
  var number = parseFloat(string)
  return isNaN(number) ? 0 : number
}

function updateDifference() {
  var minuend = document.querySelector(".js-substraction-minuend").innerHTML
  var subtrahend = document.querySelector(".js-substraction-subtrahend").innerHTML
  var difference = document.querySelector(".js-substraction-difference")
  minuend = parseNumber(minuend)
  subtrahend = parseNumber(subtrahend)
  var result = minuend - subtrahend;
  difference.innerHTML = result.toLocaleString("de", { style: "currency", currency: "EUR" })
}

document.querySelectorAll(".js-sum").forEach(function (fieldset) {
  var inputs = fieldset.querySelectorAll('input')
  inputs.forEach(function (input) {
    input.addEventListener("input", function () {
      setTimeout(updateDifference, 1);
    });
  })
  setTimeout(updateDifference, 1);
})