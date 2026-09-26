import { getZodiacSign, parseDob, generateLocalHoroscope, ZODIAC_DATA } from './horoscopeEngine';

describe('Cloud Horoscope Engine', () => {
  test('accurately parses dates in various formats', () => {
    expect(parseDob('1995-05-15')).toEqual({
      day: 15,
      month: 5,
      year: 1995,
      formatted: '15/05/1995'
    });

    expect(parseDob('15/05/1995')).toEqual({
      day: 15,
      month: 5,
      year: 1995,
      formatted: '15/05/1995'
    });
  });

  test('determines all 12 zodiac signs accurately', () => {
    expect(getZodiacSign(21, 3)).toBe('Aries');
    expect(getZodiacSign(20, 4)).toBe('Taurus');
    expect(getZodiacSign(21, 5)).toBe('Gemini');
    expect(getZodiacSign(21, 6)).toBe('Cancer');
    expect(getZodiacSign(23, 7)).toBe('Leo');
    expect(getZodiacSign(23, 8)).toBe('Virgo');
    expect(getZodiacSign(23, 9)).toBe('Libra');
    expect(getZodiacSign(23, 10)).toBe('Scorpio');
    expect(getZodiacSign(22, 11)).toBe('Sagittarius');
    expect(getZodiacSign(22, 12)).toBe('Capricorn');
    expect(getZodiacSign(15, 1)).toBe('Capricorn');
    expect(getZodiacSign(20, 1)).toBe('Aquarius');
    expect(getZodiacSign(19, 2)).toBe('Pisces');
  });

  test('generates rich cloud-themed horoscope reading', () => {
    const reading = generateLocalHoroscope('Satoshi', '1990-07-25');
    expect(reading.sign).toBe('Leo');
    expect(reading.symbol).toBe('♌');
    expect(reading.element).toBe('Fire');
    expect(reading.luckyService).toBeDefined();
    expect(reading.luckyRegion).toBeDefined();
    expect(reading.horoscope).toContain('Satoshi');
  });
});
