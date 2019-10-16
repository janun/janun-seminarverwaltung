// fieldsets with a class of 'js-sum' will get all their inputs summed on input
// and the result saved in the first readonly field

function sum(list) {
    return list.reduce(function (pv, cv) { return pv + cv }, 0)
}

function updateTotal(from_fields, to_field) {
    var values = Array.from(from_fields, function (field) {
        return parseFloat(field.value)
    }).filter(function (value) {
        return !Number.isNaN(value)
    })
    to_field.innerHTML = sum(values).toLocaleString("de", { useGrouping: false })
}

document.querySelectorAll(".js-sum").forEach(function (fieldset) {
    var inputs = fieldset.querySelectorAll('input')
    var output = fieldset.querySelector('.readonly')
    inputs.forEach(function (input) {
        input.addEventListener("input", function () {
            updateTotal(inputs, output)
        });
    })
})