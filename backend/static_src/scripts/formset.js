document.querySelectorAll('.js-formset').forEach(function (formset) {

  var AddButton = formset.querySelector('.formset-add')
  var template = formset.querySelector('.formset-template').innerHTML
  var list = formset.querySelector('.formset-list')

  AddButton.addEventListener('click', function (event) {
    event.preventDefault()
    var count = list.childElementCount
    template = template.replace(/__prefix__/g, count)
    list.insertAdjacentHTML('beforeend', template)

    var totalForms = formset.querySelector('[id$=TOTAL_FORMS]')
    totalForms.setAttribute('value', count + 1)
    attachDelete()
  })

  function attachDelete() {
    // hide original delete checkbox
    formset.querySelectorAll('[id$=DELETE]').forEach(function (checkbox) {
      checkbox.style.display = "none"
    })

    // dynamically added
    formset.querySelectorAll('.formset-delete').forEach(function (deleteButton) {
      deleteButton.addEventListener('click', function (event) {
        event.preventDefault()
        var row = deleteButton.closest('.formset-row')
        row.remove()

        var totalForms = formset.querySelector('[id$=TOTAL_FORMS]')
        var count = list.childElementCount
        totalForms.setAttribute('value', count - 1)
      })
    })

    // already in django db -> use the checkbox
    formset.querySelectorAll('.formset-django-delete').forEach(function (deleteButton) {
      deleteButton.addEventListener('click', function (event) {
        event.preventDefault()
        var row = deleteButton.closest('.formset-row')
        row.className = "hidden"

        var checkbox = row.querySelector('input[id$="-DELETE"]')
        checkbox.checked = true
      })
    })
  }
  attachDelete()
})

