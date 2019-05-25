// compare two arbitrary values for equality
export function objectCompare(obj1, obj2) {
  // use simple compare if not an object
  if (typeof obj1 !== 'object' && typeof obj2 !== 'object') {
    return obj1 == obj2 // eslint-disable-line eqeqeq
  }

  return JSON.stringify(obj1) === JSON.stringify(obj2)
}
