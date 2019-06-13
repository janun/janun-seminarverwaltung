function nonGroupLimit(days) {
  return Math.min(1000, 450 + 200 * Math.max(0, days - 3))
}

function nonGroupFundingRate(days) {
  return days === 1 ? 8 : 10
}

function nonGroupFunding(days, attendees) {
  const funding = attendees * days * nonGroupFundingRate(days)
  return Math.min(nonGroupLimit(days), funding)
}

function groupFundingRate(days) {
  return days === 1 ? 8 : 13.5
}

function groupFunding(days, attendees) {
  return attendees * days * groupFundingRate(days)
}

export function getMaxFunding(days, group, attendees) {
  if (typeof days === 'string') {
    days = parseInt(days, 10)
  }
  if (typeof attendees === 'string') {
    attendees = parseInt(attendees, 10)
  }
  if (group) {
    return groupFunding(days, attendees)
  }
  return nonGroupFunding(days, attendees)
}
