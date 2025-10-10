"""
Unit tests for zodiac calculation functionality
"""

import unittest
from datetime import datetime
from lambda_function import get_zodiac_sign, ZODIAC_RANGES


class TestZodiacCalculation(unittest.TestCase):
    """Test cases for zodiac sign calculation"""
    
    def test_all_zodiac_signs_with_boundary_dates(self):
        """Test all 12 zodiac signs with their boundary dates"""
        
        # Test each zodiac sign with start and end boundary dates
        test_cases = [
            # Aries: March 21 - April 19
            (21, 3, "Aries"),  # Start boundary
            (19, 4, "Aries"),  # End boundary
            (30, 3, "Aries"),  # Middle date
            
            # Taurus: April 20 - May 20
            (20, 4, "Taurus"),  # Start boundary
            (20, 5, "Taurus"),  # End boundary
            (1, 5, "Taurus"),   # Middle date
            
            # Gemini: May 21 - June 20
            (21, 5, "Gemini"),  # Start boundary
            (20, 6, "Gemini"),  # End boundary
            (10, 6, "Gemini"),  # Middle date
            
            # Cancer: June 21 - July 22
            (21, 6, "Cancer"),  # Start boundary
            (22, 7, "Cancer"),  # End boundary
            (1, 7, "Cancer"),   # Middle date
            
            # Leo: July 23 - August 22
            (23, 7, "Leo"),     # Start boundary
            (22, 8, "Leo"),     # End boundary
            (15, 8, "Leo"),     # Middle date
            
            # Virgo: August 23 - September 22
            (23, 8, "Virgo"),   # Start boundary
            (22, 9, "Virgo"),   # End boundary
            (10, 9, "Virgo"),   # Middle date
            
            # Libra: September 23 - October 22
            (23, 9, "Libra"),   # Start boundary
            (22, 10, "Libra"),  # End boundary
            (15, 10, "Libra"),  # Middle date
            
            # Scorpio: October 23 - November 21
            (23, 10, "Scorpio"), # Start boundary
            (21, 11, "Scorpio"), # End boundary
            (10, 11, "Scorpio"), # Middle date
            
            # Sagittarius: November 22 - December 21
            (22, 11, "Sagittarius"), # Start boundary
            (21, 12, "Sagittarius"), # End boundary
            (10, 12, "Sagittarius"), # Middle date
            
            # Capricorn: December 22 - January 19 (year boundary case)
            (22, 12, "Capricorn"), # Start boundary (December)
            (19, 1, "Capricorn"),  # End boundary (January)
            (31, 12, "Capricorn"), # Middle date (December)
            (10, 1, "Capricorn"),  # Middle date (January)
            
            # Aquarius: January 20 - February 18
            (20, 1, "Aquarius"),  # Start boundary
            (18, 2, "Aquarius"),  # End boundary
            (1, 2, "Aquarius"),   # Middle date
            
            # Pisces: February 19 - March 20
            (19, 2, "Pisces"),    # Start boundary
            (20, 3, "Pisces"),    # End boundary
            (28, 2, "Pisces"),    # Middle date
        ]
        
        for day, month, expected_sign in test_cases:
            with self.subTest(day=day, month=month, expected_sign=expected_sign):
                result = get_zodiac_sign(day, month)
                self.assertEqual(result, expected_sign, 
                               f"Expected {expected_sign} for {day}/{month}, got {result}")
    
    def test_leap_year_scenarios(self):
        """Test leap year scenarios and edge cases"""
        
        # Test February 29th (leap year) - should be Pisces
        result = get_zodiac_sign(29, 2)
        self.assertEqual(result, "Pisces", "February 29th should be Pisces")
        
        # Test dates around leap year boundary
        leap_year_cases = [
            (28, 2, "Pisces"),    # Feb 28 - always Pisces
            (29, 2, "Pisces"),    # Feb 29 - Pisces in leap years
            (1, 3, "Pisces"),     # Mar 1 - Pisces
            (19, 2, "Pisces"),    # Feb 19 - Pisces start boundary
            (20, 3, "Pisces"),    # Mar 20 - Pisces end boundary
            (21, 3, "Aries"),     # Mar 21 - Aries start boundary
        ]
        
        for day, month, expected_sign in leap_year_cases:
            with self.subTest(day=day, month=month, expected_sign=expected_sign):
                result = get_zodiac_sign(day, month)
                self.assertEqual(result, expected_sign,
                               f"Expected {expected_sign} for {day}/{month}, got {result}")
    
    def test_year_boundary_edge_cases(self):
        """Test edge cases around year boundaries, especially Capricorn"""
        
        year_boundary_cases = [
            # Test Capricorn year boundary
            (21, 12, "Sagittarius"), # Dec 21 - last day of Sagittarius
            (22, 12, "Capricorn"),   # Dec 22 - first day of Capricorn
            (31, 12, "Capricorn"),   # Dec 31 - middle of Capricorn
            (1, 1, "Capricorn"),     # Jan 1 - middle of Capricorn
            (19, 1, "Capricorn"),    # Jan 19 - last day of Capricorn
            (20, 1, "Aquarius"),     # Jan 20 - first day of Aquarius
            
            # Test other boundary transitions
            (20, 3, "Pisces"),       # Mar 20 - last day of Pisces
            (21, 3, "Aries"),        # Mar 21 - first day of Aries
            (19, 4, "Aries"),        # Apr 19 - last day of Aries
            (20, 4, "Taurus"),       # Apr 20 - first day of Taurus
        ]
        
        for day, month, expected_sign in year_boundary_cases:
            with self.subTest(day=day, month=month, expected_sign=expected_sign):
                result = get_zodiac_sign(day, month)
                self.assertEqual(result, expected_sign,
                               f"Expected {expected_sign} for {day}/{month}, got {result}")
    
    def test_invalid_input_validation(self):
        """Test that invalid inputs raise appropriate errors"""
        
        # Test invalid months
        invalid_month_cases = [0, 13, -1, 15]
        for invalid_month in invalid_month_cases:
            with self.subTest(month=invalid_month):
                with self.assertRaises(ValueError) as context:
                    get_zodiac_sign(15, invalid_month)
                self.assertIn("Invalid month", str(context.exception))
        
        # Test invalid days
        invalid_day_cases = [0, 32, -1, 50]
        for invalid_day in invalid_day_cases:
            with self.subTest(day=invalid_day):
                with self.assertRaises(ValueError) as context:
                    get_zodiac_sign(invalid_day, 6)
                self.assertIn("Invalid day", str(context.exception))
    
    def test_zodiac_ranges_completeness(self):
        """Test that ZODIAC_RANGES covers all possible dates without gaps"""
        
        # Test a sampling of dates throughout the year to ensure no gaps
        test_dates = [
            (1, 1), (15, 1), (31, 1),    # January
            (1, 2), (14, 2), (28, 2),    # February
            (1, 3), (15, 3), (31, 3),    # March
            (1, 4), (15, 4), (30, 4),    # April
            (1, 5), (15, 5), (31, 5),    # May
            (1, 6), (15, 6), (30, 6),    # June
            (1, 7), (15, 7), (31, 7),    # July
            (1, 8), (15, 8), (31, 8),    # August
            (1, 9), (15, 9), (30, 9),    # September
            (1, 10), (15, 10), (31, 10), # October
            (1, 11), (15, 11), (30, 11), # November
            (1, 12), (15, 12), (31, 12), # December
        ]
        
        for day, month in test_dates:
            with self.subTest(day=day, month=month):
                # Should not raise an exception for any valid date
                result = get_zodiac_sign(day, month)
                self.assertIsInstance(result, str)
                self.assertIn(result, [sign for _, _, sign in ZODIAC_RANGES])
    
    def test_zodiac_ranges_data_structure(self):
        """Test that ZODIAC_RANGES data structure is correctly formatted"""
        
        # Verify we have exactly 12 zodiac signs
        self.assertEqual(len(ZODIAC_RANGES), 12, "Should have exactly 12 zodiac signs")
        
        # Verify all expected zodiac signs are present
        expected_signs = {
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        }
        actual_signs = {sign for _, _, sign in ZODIAC_RANGES}
        self.assertEqual(actual_signs, expected_signs, "All zodiac signs should be present")
        
        # Verify data structure format
        for start, end, sign in ZODIAC_RANGES:
            with self.subTest(sign=sign):
                # Check start date format
                self.assertIsInstance(start, tuple)
                self.assertEqual(len(start), 2)
                start_month, start_day = start
                self.assertIsInstance(start_month, int)
                self.assertIsInstance(start_day, int)
                self.assertTrue(1 <= start_month <= 12)
                self.assertTrue(1 <= start_day <= 31)
                
                # Check end date format
                self.assertIsInstance(end, tuple)
                self.assertEqual(len(end), 2)
                end_month, end_day = end
                self.assertIsInstance(end_month, int)
                self.assertIsInstance(end_day, int)
                self.assertTrue(1 <= end_month <= 12)
                self.assertTrue(1 <= end_day <= 31)
                
                # Check sign is string
                self.assertIsInstance(sign, str)
                self.assertTrue(len(sign) > 0)


if __name__ == '__main__':
    unittest.main()