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

export function objectCompare(obj1: object, obj2: object): boolean {
  for (const p in obj1) {
    if (obj1.hasOwnProperty(p)) {
      if (!obj2.hasOwnProperty(p)) {
        return false;
      }
      switch (typeof obj1[p as keyof object]) {
        // Deep compare objects
        case 'object':
          if (!objectCompare(obj1[p as keyof object], obj2[p as keyof object])) {
            return false;
          }
          break;
        // Compare values
        default:
          if (obj1[p as keyof object] !== obj2[p as keyof object]) {
            return false;
          }
      }
    }
  }
  for (const p in obj2) {
    if (typeof obj1[p as keyof object] === 'undefined') {
      return false;
    }
  }
  return true;
}
