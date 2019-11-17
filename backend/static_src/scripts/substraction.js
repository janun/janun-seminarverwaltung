function updateDifference() {
  var minuend = document.querySelector(".js-substraction-minuend").innerHTML.replace('.', '').replace(',', '.');
  var subtrahend = document.querySelector(".js-substraction-subtrahend").innerHTML.replace('.', '').replace(',', '.');
  var difference = document.querySelector(".js-substraction-difference");
  minuend = isNaN(minuend) ? 0 : parseFloat(minuend);
  subtrahend = isNaN(subtrahend) ? 0 : parseFloat(subtrahend);
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