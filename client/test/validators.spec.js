import { notSimiliarTo } from '@/utils/validators.js'

describe('notSimiliarTo', () => {
  test('is not required', () => {
    expect(notSimiliarTo('testString')()).toBeTruthy()
    expect(notSimiliarTo()('testString')).toBeTruthy()
  })

  test('rejects equal strings', () => {
    expect(notSimiliarTo('testString')('testString')).toBeFalsy()
  })

  test('rejects similiar strings', () => {
    expect(notSimiliarTo('testStrinl')('testStrins')).toBeFalsy()
  })

  test('rejects start of email', () => {
    expect(notSimiliarTo('mustermann@example.com')('musterman')).toBeFalsy()
  })
})
