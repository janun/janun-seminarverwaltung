var incomeField = document.querySelector(".field-formatted_income_total .readonly")
var expenseField = document.querySelector(".field-formatted_expense_total .readonly")
var toField = document.querySelector(".field-formatted_expense_minus_income .readonly")

function parseStrToFloat(str) {
    return parseFloat(str.replace(',', '.'))
}

function updateExpenseMinusIncome() {
    result = parseStrToFloat(expenseField.innerText) - parseStrToFloat(incomeField.innerText);
    toField.innerText = result.toLocaleString("de", { useGrouping: false })
}

document.querySelectorAll(".js-sum").forEach(function (fieldset) {
    var inputs = fieldset.querySelectorAll('input')
    inputs.forEach(function (input) {
        input.addEventListener("input", function () {
            updateExpenseMinusIncome()
        });
    })
})