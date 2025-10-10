"""
Test response formatting functions
"""

import json
import unittest
from datetime import datetime
from unittest.mock import Mock

from lambda_function import (
    format_success_response,
    format_error_response,
    handle_validation_error,
    handle_service_error,
    handle_system_error
)


class TestResponseFormatting(unittest.TestCase):
    """Test response formatting functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_context = Mock()
        self.mock_context.aws_request_id = "test-request-123"
    
    def test_format_success_response(self):
        """Test successful response formatting"""
        response = format_success_response(
            project="Cloud Horoscope",
            author="Test Author",
            sign="Libra",
            horoscope="Your AWS Lambda functions will scale beautifully today!"
        )
        
        # Check response structure
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Content-Type", response["headers"])
        self.assertEqual(response["headers"]["Content-Type"], "application/json")
        self.assertIn("Access-Control-Allow-Origin", response["headers"])
        
        # Parse and check body
        body = json.loads(response["body"])
        self.assertEqual(body["project"], "Cloud Horoscope")
        self.assertEqual(body["author"], "Test Author")
        self.assertEqual(body["sign"], "Libra")
        self.assertEqual(body["horoscope"], "Your AWS Lambda functions will scale beautifully today!")
    
    def test_format_error_response_basic(self):
        """Test basic error response formatting"""
        response = format_error_response("Test error message", 400)
        
        # Check response structure
        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Content-Type", response["headers"])
        self.assertEqual(response["headers"]["Content-Type"], "application/json")
        
        # Parse and check body
        body = json.loads(response["body"])
        self.assertEqual(body["error"], "Test error message")
        self.assertIn("timestamp", body)
        # Should not have request_id without context
        self.assertNotIn("request_id", body)
    
    def test_format_error_response_with_context(self):
        """Test error response formatting with context"""
        response = format_error_response("Test error", 500, self.mock_context)
        
        # Parse and check body
        body = json.loads(response["body"])
        self.assertEqual(body["error"], "Test error")
        self.assertEqual(body["request_id"], "test-request-123")
        self.assertIn("timestamp", body)
    
    def test_handle_validation_error(self):
        """Test validation error handling"""
        error = ValueError("Invalid input format")
        response = handle_validation_error(error, self.mock_context)
        
        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertEqual(body["error"], "Invalid input format")
        self.assertEqual(body["request_id"], "test-request-123")
    
    def test_handle_service_error_rate_limiting(self):
        """Test service error handling for rate limiting"""
        error = Exception("Rate limiting error occurred")
        response = handle_service_error(error, self.mock_context)
        
        self.assertEqual(response["statusCode"], 429)
        body = json.loads(response["body"])
        self.assertEqual(body["error"], "Too many requests. Please try again later.")
    
    def test_handle_service_error_service_unavailable(self):
        """Test service error handling for service unavailable"""
        error = Exception("Service unavailable at this time")
        response = handle_service_error(error, self.mock_context)
        
        self.assertEqual(response["statusCode"], 503)
        body = json.loads(response["body"])
        self.assertEqual(body["error"], "AI service temporarily unavailable. Please try again.")
    
    def test_handle_service_error_timeout(self):
        """Test service error handling for timeout"""
        error = Exception("Request timeout occurred")
        response = handle_service_error(error, self.mock_context)
        
        self.assertEqual(response["statusCode"], 504)
        body = json.loads(response["body"])
        self.assertEqual(body["error"], "Request timeout. Please try again.")
    
    def test_handle_service_error_generic(self):
        """Test service error handling for generic errors"""
        error = Exception("Some other service error")
        response = handle_service_error(error, self.mock_context)
        
        self.assertEqual(response["statusCode"], 500)
        body = json.loads(response["body"])
        self.assertEqual(body["error"], "Error generating horoscope. Please try again.")
    
    def test_handle_system_error(self):
        """Test system error handling"""
        error = Exception("Unexpected system error")
        response = handle_system_error(error, self.mock_context)
        
        self.assertEqual(response["statusCode"], 500)
        body = json.loads(response["body"])
        self.assertEqual(body["error"], "Internal server error. Please try again.")
        self.assertEqual(body["request_id"], "test-request-123")
    
    def test_success_response_api_gateway_compatibility(self):
        """Test success response is API Gateway compatible (Requirement 4.1, 4.2)"""
        response = format_success_response(
            project="Test Project",
            author="Test Author", 
            sign="Aries",
            horoscope="Test horoscope"
        )
        
        # Requirement 4.1: statusCode 200
        self.assertEqual(response["statusCode"], 200)
        
        # API Gateway compatibility - must have headers
        self.assertIn("headers", response)
        self.assertIn("body", response)
        
        # CORS headers for web integration
        self.assertEqual(response["headers"]["Access-Control-Allow-Origin"], "*")
        
        # Requirement 4.2: body contains required fields
        body = json.loads(response["body"])
        required_fields = ["project", "author", "sign", "horoscope"]
        for field in required_fields:
            self.assertIn(field, body)
    
    def test_error_response_400_status_code(self):
        """Test error response returns 400 status code (Requirement 5.1)"""
        response = format_error_response("Invalid date format. Please use dd/mm/yyyy.", 400)
        
        # Requirement 5.1: 400 status code for invalid date format
        self.assertEqual(response["statusCode"], 400)
        
        # API Gateway compatibility
        self.assertIn("headers", response)
        self.assertIn("body", response)
        
        # Requirement 5.2: error field with specific message
        body = json.loads(response["body"])
        self.assertIn("error", body)
        self.assertEqual(body["error"], "Invalid date format. Please use dd/mm/yyyy.")
    
    def test_error_response_structured_format(self):
        """Test error response has structured format (Requirement 5.2)"""
        response = format_error_response("Test error message", 400, self.mock_context)
        
        # Must be valid JSON
        body = json.loads(response["body"])
        
        # Required error response fields
        self.assertIn("error", body)
        self.assertIn("timestamp", body)
        self.assertIn("request_id", body)
        
        # Timestamp should be ISO format
        timestamp = body["timestamp"]
        # Should not raise exception when parsing
        datetime.fromisoformat(timestamp.replace('Z', '+00:00') if timestamp.endswith('Z') else timestamp)
    
    def test_success_response_environment_variable_defaults(self):
        """Test success response uses environment variable defaults (Requirements 4.4, 4.5)"""
        # Test with default values that would come from environment
        response = format_success_response(
            project="Cloud Horoscope",  # Default from PROJECT_NAME
            author="Unknown Author",    # Default from AUTHOR_NAME
            sign="Leo",
            horoscope="Your EC2 instances are aligned with the stars!"
        )
        
        body = json.loads(response["body"])
        self.assertEqual(body["project"], "Cloud Horoscope")
        self.assertEqual(body["author"], "Unknown Author")
    
    def test_error_response_no_crash_on_parsing_error(self):
        """Test error responses don't crash system (Requirement 5.5)"""
        # Test various error scenarios that should not crash
        test_errors = [
            ("Missing field error", 400),
            ("Invalid JSON format", 400),
            ("Service unavailable", 503),
            ("Internal error", 500)
        ]
        
        for error_msg, status_code in test_errors:
            response = format_error_response(error_msg, status_code, self.mock_context)
            
            # Should always return valid response structure
            self.assertIn("statusCode", response)
            self.assertIn("headers", response)
            self.assertIn("body", response)
            self.assertEqual(response["statusCode"], status_code)
            
            # Body should be valid JSON
            body = json.loads(response["body"])
            self.assertIn("error", body)
            self.assertEqual(body["error"], error_msg)


if __name__ == '__main__':
    unittest.main()