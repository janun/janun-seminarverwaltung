var fundingField = document.querySelector('#id_requested_funding');
var startDateField = document.querySelector('#id_start_date');

// update funding in confirmation checkbox
function updateFunding() {
  var funding = parseFloat(fundingField.value);
  var fundingStr = funding.toLocaleString("de", { style: "currency", currency: "EUR" });
  document.querySelector('#funding').innerHTML = funding ? "von " + fundingStr : "";
}
fundingField.addEventListener('input', updateFunding);
updateFunding();


function parseGermanDate(string) {
  var parts = string.match(/^(\d{1,2})\.(\d{1,2})\.(\d{2}|\d{4})$/);
  if (parts) {
    var day = parseInt(parts[1]);
    var month = parseInt(parts[2]);
    var year = parseInt(parts[3].length === 2 ? "20" + parts[3] : parts[3]);
    var date = new Date(year, month - 1, day);
    if (date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day) {
      return date;
    }
  }
}

function getDeadline(date) {
  var quarter = Math.floor((date.getMonth() / 3));
  var year = date.getFullYear();
  var month = [4, 7, 10, 1][quarter];
  if (quarter === 3) year += 1;
  return new Date(year, month - 1, 15);
}

// update deadline in confirmation checkbox
function updateDeadline() {
  var date = parseGermanDate(startDateField.value)
  if (date) {
    document.querySelector('#deadline').innerHTML = "am " + getDeadline(date).toLocaleDateString("de");
  } else {
    document.querySelector('#deadline').innerHTML = "";
  }
}
startDateField.addEventListener('input', updateDeadline);
updateDeadline();


//var startDateField = document.querySelector("#id_start_date");
var groupField = document.querySelector('#id_group');
var daysField = document.querySelector('#id_planned_training_days');
var attendeesField = document.querySelector('#id_planned_attendees_max');

function updateMaxFunding() {
  var maxFundingText = document.querySelector('#max_funding_text');
  var maxFundingSpan = document.querySelector('#max_funding');

  var startDate = parseGermanDate(startDateField.value)
  var year = startDate ? startDate.getFullYear() : undefined;
  var days = parseInt(daysField.value);
  var attendees = parseInt(attendeesField.value);
  var group = groupField.value;

  if (year && days && attendees) {
    var XHR = new XMLHttpRequest();
    XHR.addEventListener('load', function (loadEvent) {
      if (loadEvent.target.status === 200) {
        var maxFunding = parseFloat(loadEvent.target.response);
        if (maxFunding) {
          maxFundingText.classList.remove('hidden');
          maxFundingSpan.innerHTML = maxFunding.toLocaleString("de", { style: "currency", currency: "EUR" });
        } else {
          maxFundingText.classList.add('hidden');
        }
      }
    });
    var url = '/seminars/calc_max_funding';
    url += "?year=" + encodeURIComponent(year);
    url += "&days=" + encodeURIComponent(days);
    url += "&group=" + encodeURIComponent(group);
    url += "&attendees=" + encodeURIComponent(attendees);
    XHR.open('GET', url);
    XHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    XHR.send();
  }
}

startDateField.addEventListener('input', updateMaxFunding);
groupField.addEventListener('change', updateMaxFunding);
daysField.addEventListener('input', updateMaxFunding);
attendeesField.addEventListener('input', updateMaxFunding);
updateMaxFunding();