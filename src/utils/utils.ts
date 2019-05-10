export function distinct<T>(values: T[]): T[] {
  return [...new Set(values)];
}

export function getFocusableChildren(el: Element): NodeListOf<HTMLElement> {
  return el.querySelectorAll(
    `button:not(:disabled),
    [href],
    input:not(:disabled),
    select:not(:disabled),
    textarea:not(:disabled),
    [tabindex]:not([tabindex="-1"])`
  );
}
