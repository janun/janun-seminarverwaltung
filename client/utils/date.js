export function getQuarter(date) {
  return Math.floor((date.getMonth() + 3) / 3)
}

const msPerDay = 24 * 3600 * 1000

function msToDays(ms) {
  return ms / msPerDay
}
function daysToMs(days) {
  return days * msPerDay
}

export function addDays(date, days) {
  return new Date(date.getTime() + daysToMs(days))
}

export function daysDiff(a, b) {
  if (typeof a === 'string') {
    a = new Date(a)
  }
  if (typeof b === 'string') {
    b = new Date(b)
  }
  return msToDays(Math.abs(a.getTime() - b.getTime()))
}

export function getDeadline(endDate) {
  if (typeof endDate === 'string') {
    endDate = new Date(endDate)
  }
  const year = endDate.getFullYear()
  const deadlines = [
    new Date(`${year}-04-15`),
    new Date(`${year}-07-15`),
    new Date(`${year}-10-15`),
    new Date(`${year + 1}-01-15`)
  ]
  return deadlines[getQuarter(endDate) - 1]
}
