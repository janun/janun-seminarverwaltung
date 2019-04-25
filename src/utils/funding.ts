function nonGroupLimit(days: number) {
  return Math.min(1000, 300 + 200 * Math.max(0, days - 3));
}

function nonGroupFundingRate(days: number) {
  return days === 1 ? 7.5 : 9;
}

function nonGroupFunding(days: number, attendees: number) {
  const funding = attendees * days * nonGroupFundingRate(days);
  return Math.min(nonGroupLimit(days), funding);
}

function groupFundingRate(days: number) {
  return days === 1 ? 7.5 : 12.5;
}

function groupFunding(days: number, attendees: number) {
  return attendees * days * groupFundingRate(days);
}

export function getMaxFunding(days: number, group: boolean, attendees: number) {
  if (group) {
    return groupFunding(days, attendees);
  }
  return nonGroupFunding(days, attendees);
}
