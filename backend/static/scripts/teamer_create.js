var fundingField = document.querySelector('#id_requested_funding');
var startDateField = document.querySelector('#id_start_date');
var endDateField = document.querySelector('#id_end_date');

// update funding in confirmation checkbox
function updateFunding() {
  var funding = parseFloat(fundingField.value);
  var fundingStr = funding.toLocaleString("de", { style: "currency", currency: "EUR" });
  var checkbox = document.querySelector('#funding');
  if (!checkbox) return;
  checkbox.innerHTML = funding ? "von " + fundingStr : "";
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

function getDeadline(startDate, endDate) {
  var quarter = Math.floor((endDate.getMonth() / 3));
  var year = endDate.getFullYear();
  var month = [4, 7, 10, 1][quarter];

  // over year boundary
  if (startDate.getMonth() == 11 && endDate.getMonth() == 0) {
    if (endDate.getDate() < 6) {
      return new Date(year, 0, 15);
    }
  }

  if (quarter === 3) year += 1;
  return new Date(year, month - 1, 15);
}

// update deadline in confirmation checkbox
function updateDeadline() {
  var endDate = parseGermanDate(endDateField.value)
  var startDate = parseGermanDate(startDateField.value)
  var checkbox = document.querySelector('#deadline');
  if (!checkbox) return;
  if (endDate) {
    checkbox.innerHTML = "am " + getDeadline(startDate, endDate).toLocaleDateString("de");
  } else {
    checkbox.innerHTML = "";
  }
}
endDateField.addEventListener('input', updateDeadline);
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