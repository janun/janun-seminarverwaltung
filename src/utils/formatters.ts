export function formatNumber(value: number | string): string {
  if (typeof value === 'string') {
    value = parseFloat(value);
  }
  return value.toLocaleString('de', { maximumFractionDigits: 1 });
}

export function formatDate(value: Date | string): string {
  if (typeof value === 'string') {
    value = new Date(value);
  }
  return value.toLocaleDateString();
}

export function formatDatetime(value: string): string {
  const date = new Date(value).toLocaleDateString();
  const time = new Date(value).toLocaleTimeString();
  return `${date} ${time}`;
}

export function formatEuro(value: number | string): string {
  if (typeof value === 'string') {
    value = parseFloat(value);
  }
  return value.toLocaleString('de-DE', {
    style: 'currency',
    currency: 'EUR'
  });
}
