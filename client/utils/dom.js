export function getFocusableChildren(el) {
  return el.querySelectorAll(
    `button:not(:disabled),
    [href],
    input:not(:disabled),
    select:not(:disabled),
    textarea:not(:disabled),
    [tabindex]:not([tabindex="-1"])`
  )
}
