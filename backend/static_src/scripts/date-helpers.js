export function parseGermanDate(string) {
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

export function dateIsoString(date) {
  var month = date.getMonth() + 1
  month = month < 10 ? "0" + month : month
  var day = date.getDate()
  day = day < 10 ? "0" + day : day
  return date.getFullYear() + '-' + month + '-' + day
}

export function formatGermanDate(date) {
  var day = date.getDate()
  day = day < 10 ? "0" + day : day
  var month = date.getMonth() + 1
  month = month < 10 ? "0" + month : month
  var year = date.getFullYear()
  return day + "." + month + "." + year
}

export function isSameDate(someDate, otherDate) {
  return someDate.getDate() === otherDate.getDate() &&
    someDate.getMonth() === otherDate.getMonth() &&
    someDate.getFullYear() === otherDate.getFullYear()
}