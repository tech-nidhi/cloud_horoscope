"""
Unit tests for input validation functionality
"""

import unittest
import json
from datetime import datetime
from lambda_function import validate_input, parse_date


class TestInputValidation(unittest.TestCase):
    """Test cases for input validation functions"""
    
    def test_valid_input_formats(self):
        """Test valid input formats that should pass validation"""
        
        valid_test_cases = [
            # Standard valid inputs
            {
                "input": {"name": "John Doe", "dob": "15/03/1990"},
                "expected_name": "John Doe",
                "expected_dob": "15/03/1990"
            },
            {
                "input": {"name": "Jane Smith", "dob": "29/02/2000"},  # Leap year
                "expected_name": "Jane Smith", 
                "expected_dob": "29/02/2000"
            },
            {
                "input": {"name": "Bob", "dob": "01/01/2000"},  # Single character name
                "expected_name": "Bob",
                "expected_dob": "01/01/2000"
            },
            {
                "input": {"name": "Alice Johnson-Brown", "dob": "31/12/1999"},  # Hyphenated name
                "expected_name": "Alice Johnson-Brown",
                "expected_dob": "31/12/1999"
            },
            {
                "input": {"name": "  Maria  ", "dob": "05/07/1985"},  # Name with spaces (should be trimmed)
                "expected_name": "Maria",
                "expected_dob": "05/07/1985"
            },
            {
                "input": {"name": "X" * 100, "dob": "10/10/1980"},  # Maximum length name (100 chars)
                "expected_name": "X" * 100,
                "expected_dob": "10/10/1980"
            },
            {
                "input": {"name": "Test User", "dob": "15/3/1990"},  # Single digit month (valid)
                "expected_name": "Test User",
                "expected_dob": "15/3/1990"
            }
        ]
        
        for i, test_case in enumerate(valid_test_cases):
            with self.subTest(test_case=i, input_data=test_case["input"]):
                event_body = json.dumps(test_case["input"])
                result = validate_input(event_body)
                
                self.assertEqual(result["name"], test_case["expected_name"])
                self.assertEqual(result["dob"], test_case["expected_dob"])
                self.assertIsInstance(result, dict)
                self.assertIn("name", result)
                self.assertIn("dob", result)
    
    def test_invalid_json_format(self):
        """Test invalid JSON formats that should raise ValueError"""
        
        invalid_json_cases = [
            "",  # Empty string
            "not json",  # Plain text
            "{invalid json}",  # Malformed JSON
            '{"name": "John", "dob": "15/03/1990"',  # Missing closing brace
            '{"name": "John" "dob": "15/03/1990"}',  # Missing comma
            "null",  # Null JSON
            "[]",  # Array instead of object
        ]
        
        for invalid_json in invalid_json_cases:
            with self.subTest(invalid_json=invalid_json):
                with self.assertRaises(ValueError) as context:
                    validate_input(invalid_json)
                self.assertIn("Invalid JSON format", str(context.exception))
    
    def test_missing_required_fields(self):
        """Test missing required fields (name and dob)"""
        
        missing_field_cases = [
            ({}, "Missing required field: name"),  # Both fields missing
            ({"dob": "15/03/1990"}, "Missing required field: name"),  # Missing name
            ({"name": "John"}, "Missing required field: dob"),  # Missing dob
            ({"other_field": "value"}, "Missing required field: name"),  # Wrong fields
        ]
        
        for input_data, expected_error in missing_field_cases:
            with self.subTest(input_data=input_data):
                event_body = json.dumps(input_data)
                with self.assertRaises(ValueError) as context:
                    validate_input(event_body)
                self.assertEqual(str(context.exception), expected_error)
    
    def test_invalid_name_validation(self):
        """Test invalid name field validation"""
        
        invalid_name_cases = [
            # Non-string names
            ({"name": 123, "dob": "15/03/1990"}, "Name must be a string"),
            ({"name": None, "dob": "15/03/1990"}, "Name must be a string"),
            ({"name": [], "dob": "15/03/1990"}, "Name must be a string"),
            ({"name": {}, "dob": "15/03/1990"}, "Name must be a string"),
            ({"name": True, "dob": "15/03/1990"}, "Name must be a string"),
            
            # Empty or whitespace names
            ({"name": "", "dob": "15/03/1990"}, "Name cannot be empty"),
            ({"name": "   ", "dob": "15/03/1990"}, "Name cannot be empty"),
            ({"name": "\t\n", "dob": "15/03/1990"}, "Name cannot be empty"),
            
            # Names too long (over 100 characters)
            ({"name": "X" * 101, "dob": "15/03/1990"}, "Name must be between 1 and 100 characters"),
            ({"name": "A" * 150, "dob": "15/03/1990"}, "Name must be between 1 and 100 characters"),
        ]
        
        for input_data, expected_error in invalid_name_cases:
            with self.subTest(input_data=input_data):
                event_body = json.dumps(input_data)
                with self.assertRaises(ValueError) as context:
                    validate_input(event_body)
                self.assertEqual(str(context.exception), expected_error)
    
    def test_invalid_dob_validation(self):
        """Test invalid date of birth field validation"""
        
        invalid_dob_cases = [
            # Non-string dob
            ({"name": "John", "dob": 20230315}, "Date of birth must be a string"),
            ({"name": "John", "dob": None}, "Date of birth must be a string"),
            ({"name": "John", "dob": []}, "Date of birth must be a string"),
            ({"name": "John", "dob": {}}, "Date of birth must be a string"),
            ({"name": "John", "dob": True}, "Date of birth must be a string"),
            
            # Invalid date formats
            ({"name": "John", "dob": "1990-03-15"}, "Invalid date format. Please use dd/mm/yyyy."),
            ({"name": "John", "dob": "15-03-1990"}, "Invalid date format. Please use dd/mm/yyyy."),
            ({"name": "John", "dob": "15/03/90"}, "Invalid date format. Please use dd/mm/yyyy."),
            ({"name": "John", "dob": "March 15, 1990"}, "Invalid date format. Please use dd/mm/yyyy."),
            ({"name": "John", "dob": "15/03"}, "Invalid date format. Please use dd/mm/yyyy."),
            ({"name": "John", "dob": "15/03/1990 10:30"}, "Invalid date format. Please use dd/mm/yyyy."),
            ({"name": "John", "dob": ""}, "Invalid date format. Please use dd/mm/yyyy."),
            ({"name": "John", "dob": "not a date"}, "Invalid date format. Please use dd/mm/yyyy."),
            
            # Invalid dates (correct format but invalid date values)
            ({"name": "John", "dob": "32/01/1990"}, "Invalid date format. Please use dd/mm/yyyy."),
            ({"name": "John", "dob": "15/13/1990"}, "Invalid date format. Please use dd/mm/yyyy."),
            ({"name": "John", "dob": "29/02/1999"}, "Invalid date format. Please use dd/mm/yyyy."),  # Not a leap year
            ({"name": "John", "dob": "31/04/1990"}, "Invalid date format. Please use dd/mm/yyyy."),  # April has 30 days
            ({"name": "John", "dob": "00/01/1990"}, "Invalid date format. Please use dd/mm/yyyy."),
            ({"name": "John", "dob": "15/00/1990"}, "Invalid date format. Please use dd/mm/yyyy."),
        ]
        
        for input_data, expected_error in invalid_dob_cases:
            with self.subTest(input_data=input_data):
                event_body = json.dumps(input_data)
                with self.assertRaises(ValueError) as context:
                    validate_input(event_body)
                self.assertEqual(str(context.exception), expected_error)
    
    def test_edge_cases_and_boundary_conditions(self):
        """Test edge cases and boundary conditions"""
        
        edge_cases = [
            # Leap year dates
            {"name": "John", "dob": "29/02/2000"},  # Valid leap year
            {"name": "Jane", "dob": "29/02/2004"},  # Valid leap year
            {"name": "Bob", "dob": "28/02/1999"},   # Valid non-leap year
            
            # Boundary dates for months with different day counts
            {"name": "Alice", "dob": "31/01/1990"},  # January 31
            {"name": "Charlie", "dob": "28/02/1990"}, # February 28 (non-leap)
            {"name": "David", "dob": "31/03/1990"},   # March 31
            {"name": "Eve", "dob": "30/04/1990"},     # April 30
            {"name": "Frank", "dob": "31/05/1990"},   # May 31
            {"name": "Grace", "dob": "30/06/1990"},   # June 30
            {"name": "Henry", "dob": "31/07/1990"},   # July 31
            {"name": "Ivy", "dob": "31/08/1990"},     # August 31
            {"name": "Jack", "dob": "30/09/1990"},    # September 30
            {"name": "Kate", "dob": "31/10/1990"},    # October 31
            {"name": "Liam", "dob": "30/11/1990"},    # November 30
            {"name": "Mia", "dob": "31/12/1990"},     # December 31
            
            # Year boundaries
            {"name": "New Year", "dob": "01/01/2000"},
            {"name": "New Year Eve", "dob": "31/12/1999"},
            
            # Name edge cases
            {"name": "A", "dob": "15/03/1990"},  # Single character name
            {"name": "X" * 100, "dob": "15/03/1990"},  # Maximum length name
        ]
        
        for test_case in edge_cases:
            with self.subTest(test_case=test_case):
                event_body = json.dumps(test_case)
                result = validate_input(event_body)
                
                # Should not raise exception and return valid result
                self.assertIsInstance(result, dict)
                self.assertIn("name", result)
                self.assertIn("dob", result)
                self.assertEqual(result["name"], test_case["name"].strip())
                self.assertEqual(result["dob"], test_case["dob"])


class TestDateParsing(unittest.TestCase):
    """Test cases specifically for date parsing functionality"""
    
    def test_valid_date_parsing(self):
        """Test valid date parsing scenarios"""
        
        valid_dates = [
            ("15/03/1990", (15, 3)),
            ("01/01/2000", (1, 1)),
            ("31/12/1999", (31, 12)),
            ("29/02/2000", (29, 2)),  # Leap year
            ("28/02/1999", (28, 2)),  # Non-leap year
            ("05/07/1985", (5, 7)),
            ("10/10/1980", (10, 10)),
            ("15/3/1990", (15, 3)),   # Single digit month
            ("5/12/1985", (5, 12)),   # Single digit day
        ]
        
        for date_string, expected_result in valid_dates:
            with self.subTest(date_string=date_string):
                result = parse_date(date_string)
                self.assertEqual(result, expected_result)
                self.assertIsInstance(result, tuple)
                self.assertEqual(len(result), 2)
                self.assertIsInstance(result[0], int)  # day
                self.assertIsInstance(result[1], int)  # month
    
    def test_invalid_date_parsing(self):
        """Test invalid date parsing scenarios"""
        
        invalid_dates = [
            # Wrong format
            "1990-03-15",  # ISO format
            "15-03-1990",  # Dashes instead of slashes
            "15/03/90",    # Two digit year
            "March 15, 1990",  # Text format
            "15/03",       # Missing year
            "15/03/1990 10:30",  # With time
            "",            # Empty string
            "not a date",  # Random text
            
            # Invalid date values
            "32/01/1990",  # Invalid day
            "15/13/1990",  # Invalid month
            "29/02/1999",  # Invalid leap year
            "31/04/1990",  # April doesn't have 31 days
            "00/01/1990",  # Zero day
            "15/00/1990",  # Zero month
        ]
        
        for invalid_date in invalid_dates:
            with self.subTest(invalid_date=invalid_date):
                with self.assertRaises(ValueError) as context:
                    parse_date(invalid_date)
                self.assertEqual(str(context.exception), "Invalid date format. Please use dd/mm/yyyy.")
    
    def test_leap_year_date_parsing(self):
        """Test leap year specific date parsing"""
        
        leap_year_cases = [
            # Valid leap years
            ("29/02/2000", (29, 2)),  # Divisible by 400
            ("29/02/2004", (29, 2)),  # Divisible by 4, not by 100
            ("29/02/1996", (29, 2)),  # Divisible by 4, not by 100
            
            # Valid non-leap year February dates
            ("28/02/1999", (28, 2)),  # Not divisible by 4
            ("28/02/1900", (28, 2)),  # Divisible by 100, not by 400
            ("28/02/2001", (28, 2)),  # Not divisible by 4
        ]
        
        for date_string, expected_result in leap_year_cases:
            with self.subTest(date_string=date_string):
                result = parse_date(date_string)
                self.assertEqual(result, expected_result)
        
        # Invalid leap year cases
        invalid_leap_cases = [
            "29/02/1999",  # 1999 is not a leap year
            "29/02/1900",  # 1900 is not a leap year (divisible by 100, not 400)
            "29/02/2001",  # 2001 is not a leap year
        ]
        
        for invalid_date in invalid_leap_cases:
            with self.subTest(invalid_date=invalid_date):
                with self.assertRaises(ValueError) as context:
                    parse_date(invalid_date)
                self.assertEqual(str(context.exception), "Invalid date format. Please use dd/mm/yyyy.")
    
    def test_boundary_date_parsing(self):
        """Test boundary dates for each month"""
        
        boundary_cases = [
            # First and last day of each month
            ("01/01/2000", (1, 1)),   # January 1st
            ("31/01/2000", (31, 1)),  # January 31st
            ("01/02/2000", (1, 2)),   # February 1st
            ("29/02/2000", (29, 2)),  # February 29th (leap year)
            ("01/03/2000", (1, 3)),   # March 1st
            ("31/03/2000", (31, 3)),  # March 31st
            ("01/04/2000", (1, 4)),   # April 1st
            ("30/04/2000", (30, 4)),  # April 30th
            ("01/05/2000", (1, 5)),   # May 1st
            ("31/05/2000", (31, 5)),  # May 31st
            ("01/06/2000", (1, 6)),   # June 1st
            ("30/06/2000", (30, 6)),  # June 30th
            ("01/07/2000", (1, 7)),   # July 1st
            ("31/07/2000", (31, 7)),  # July 31st
            ("01/08/2000", (1, 8)),   # August 1st
            ("31/08/2000", (31, 8)),  # August 31st
            ("01/09/2000", (1, 9)),   # September 1st
            ("30/09/2000", (30, 9)),  # September 30th
            ("01/10/2000", (1, 10)),  # October 1st
            ("31/10/2000", (31, 10)), # October 31st
            ("01/11/2000", (1, 11)),  # November 1st
            ("30/11/2000", (30, 11)), # November 30th
            ("01/12/2000", (1, 12)),  # December 1st
            ("31/12/2000", (31, 12)), # December 31st
        ]
        
        for date_string, expected_result in boundary_cases:
            with self.subTest(date_string=date_string):
                result = parse_date(date_string)
                self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()