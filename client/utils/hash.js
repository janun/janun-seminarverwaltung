export function sha1(string) {
  const buffer = new TextEncoder('utf-8').encode(string)
  return crypto.subtle.digest('SHA-1', buffer).then(function(buffer) {
    // Get the hex code
    const hexCodes = []
    const view = new DataView(buffer)
    for (let i = 0; i < view.byteLength; i += 4) {
      // Using getUint32 reduces the number of iterations needed (we process 4 bytes each time)
      const value = view.getUint32(i)
      // toString(16) will give the hex representation of the number without padding
      const stringValue = value.toString(16)
      // We use concatenation and slice for padding
      const padding = '00000000'
      const paddedValue = (padding + stringValue).slice(-padding.length)
      hexCodes.push(paddedValue)
    }
    // Join all the hex strings into one
    return hexCodes.join('')
  })
}
