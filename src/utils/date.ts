export function getQuarter(date: Date): number {
  return Math.floor((date.getMonth() + 3) / 3);
}

const msPerDay = 24 * 3600 * 1000;

function msToDays(ms: number): number {
  return ms / msPerDay;
}
function daysToMs(days: number): number {
  return days * msPerDay;
}

export function addDays(date: Date, days: number): Date {
  return new Date(date.getTime() + daysToMs(days));
}

export function daysDiff(a: Date, b: Date): number {
  return msToDays(Math.abs(a.getTime() - b.getTime()));
}

export function getDeadline(endDate: Date): Date {
  endDate = new Date(endDate);
  const year = endDate.getFullYear();
  const deadlines = [
    new Date(`${year}-04-15`),
    new Date(`${year}-07-15`),
    new Date(`${year}-10-15`),
    new Date(`${year + 1}-01-15`)
  ];
  return deadlines[getQuarter(endDate) - 1];
}
