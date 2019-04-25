export function formatNumber(value: number): string {
  return value.toLocaleString('de', { maximumFractionDigits: 1 });
}

export function formatDate(value: string): string {
  return new Date(value).toLocaleDateString();
}

export function formatDatetime(value: string): string {
  const date = new Date(value).toLocaleDateString();
  const time = new Date(value).toLocaleTimeString();
  return `${date} ${time}`;
}

export function formatEuro(value: number): string {
  return value.toLocaleString('de-DE', {
    style: 'currency',
    currency: 'EUR'
  });
}
