"""
Integration tests for complete Lambda handler
Tests end-to-end request processing with various input scenarios and error cases
"""

import json
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from lambda_function import lambda_handler


class TestIntegrationHandler(unittest.TestCase):
    """Integration tests for complete Lambda handler end-to-end processing"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock Lambda context
        self.mock_context = Mock()
        self.mock_context.aws_request_id = "test-request-id-12345"
        
        # Sample valid input
        self.valid_input = {
            "name": "John Doe",
            "dob": "15/03/1990"
        }
        
        # Sample API Gateway event structure
        self.base_event = {
            "body": json.dumps(self.valid_input),
            "headers": {"Content-Type": "application/json"},
            "httpMethod": "POST",
            "path": "/horoscope"
        }
        
        # Mock Bedrock response
        self.mock_bedrock_response = {
            "body": Mock()
        }
        self.mock_bedrock_response["body"].read.return_value = json.dumps({
            "content": [
                {
                    "text": "Your Lambda functions are aligned with the stars today! "
                           "S3 buckets overflow with cosmic energy, and EC2 instances "
                           "dance in perfect harmony. A CloudFront distribution "
                           "brings good fortune from distant regions."
                }
            ]
        }).encode('utf-8')
    
    @patch('lambda_function.bedrock_client')
    @patch('lambda_function.config')
    def test_successful_end_to_end_processing(self, mock_config, mock_bedrock_client):
        """Test complete successful request processing from input to response"""
        # Arrange
        mock_config.get_project_name.return_value = "Cloud Horoscope"
        mock_config.get_author_name.return_value = "Test Author"
        mock_config.get_bedrock_config.return_value = {
            'model_id': 'anthropic.claude-3-haiku-20240307',
            'region': 'us-east-1',
            'max_tokens': 200,
            'temperature': 0.7
        }
        mock_bedrock_client.invoke_model.return_value = self.mock_bedrock_response
        
        # Act
        response = lambda_handler(self.base_event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Content-Type", response["headers"])
        self.assertEqual(response["headers"]["Content-Type"], "application/json")
        
        # Parse response body
        response_body = json.loads(response["body"])
        
        # Verify all required fields are present
        self.assertIn("project", response_body)
        self.assertIn("author", response_body)
        self.assertIn("sign", response_body)
        self.assertIn("horoscope", response_body)
        
        # Verify field values
        self.assertEqual(response_body["project"], "Cloud Horoscope")
        self.assertEqual(response_body["author"], "Test Author")
        self.assertEqual(response_body["sign"], "Pisces")  # March 15 is Pisces
        self.assertIn("Lambda", response_body["horoscope"])  # Should contain AWS services
        
        # Verify Bedrock was called correctly
        mock_bedrock_client.invoke_model.assert_called_once()
        call_args = mock_bedrock_client.invoke_model.call_args
        self.assertIn("modelId", call_args.kwargs)
        self.assertEqual(call_args.kwargs["contentType"], "application/json")
        self.assertEqual(call_args.kwargs["accept"], "application/json")
    
    def test_missing_request_body(self):
        """Test handling of missing request body"""
        # Arrange
        event_without_body = {"headers": {"Content-Type": "application/json"}}
        
        # Act
        response = lambda_handler(event_without_body, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Missing required field", response_body["error"])
    
    def test_null_request_body(self):
        """Test handling of null request body"""
        # Arrange
        event_with_null_body = {"body": None}
        
        # Act
        response = lambda_handler(event_with_null_body, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Missing required field", response_body["error"])
    
    def test_invalid_json_format(self):
        """Test handling of invalid JSON in request body"""
        # Arrange
        event_with_invalid_json = {"body": "invalid json {"}
        
        # Act
        response = lambda_handler(event_with_invalid_json, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Invalid JSON format", response_body["error"])
    
    def test_missing_name_field(self):
        """Test handling of missing name field"""
        # Arrange
        invalid_input = {"dob": "15/03/1990"}
        event = {"body": json.dumps(invalid_input)}
        
        # Act
        response = lambda_handler(event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Missing required field: name", response_body["error"])
    
    def test_missing_dob_field(self):
        """Test handling of missing date of birth field"""
        # Arrange
        invalid_input = {"name": "John Doe"}
        event = {"body": json.dumps(invalid_input)}
        
        # Act
        response = lambda_handler(event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Missing required field: dob", response_body["error"])
    
    def test_empty_name_field(self):
        """Test handling of empty name field"""
        # Arrange
        invalid_input = {"name": "", "dob": "15/03/1990"}
        event = {"body": json.dumps(invalid_input)}
        
        # Act
        response = lambda_handler(event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Name cannot be empty", response_body["error"])
    
    def test_name_too_long(self):
        """Test handling of name field that exceeds maximum length"""
        # Arrange
        long_name = "A" * 101  # 101 characters, exceeds 100 character limit
        invalid_input = {"name": long_name, "dob": "15/03/1990"}
        event = {"body": json.dumps(invalid_input)}
        
        # Act
        response = lambda_handler(event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Name must be between 1 and 100 characters", response_body["error"])
    
    def test_invalid_date_format(self):
        """Test handling of invalid date format"""
        # Arrange
        invalid_input = {"name": "John Doe", "dob": "1990-03-15"}  # Wrong format
        event = {"body": json.dumps(invalid_input)}
        
        # Act
        response = lambda_handler(event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Invalid date format. Please use dd/mm/yyyy", response_body["error"])
    
    def test_invalid_date_values(self):
        """Test handling of invalid date values"""
        # Arrange
        invalid_input = {"name": "John Doe", "dob": "32/13/1990"}  # Invalid day and month
        event = {"body": json.dumps(invalid_input)}
        
        # Act
        response = lambda_handler(event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Invalid date format. Please use dd/mm/yyyy", response_body["error"])
    
    def test_leap_year_date_processing(self):
        """Test processing of leap year date (February 29th)"""
        # Arrange
        leap_year_input = {"name": "Jane Doe", "dob": "29/02/2000"}
        event = {"body": json.dumps(leap_year_input)}
        
        with patch('lambda_function.bedrock_client') as mock_bedrock_client, \
             patch('lambda_function.config') as mock_config:
            
            mock_config.get_project_name.return_value = "Cloud Horoscope"
            mock_config.get_author_name.return_value = "Test Author"
            mock_config.get_bedrock_config.return_value = {
                'model_id': 'anthropic.claude-3-haiku-20240307',
                'region': 'us-east-1',
                'max_tokens': 200,
                'temperature': 0.7
            }
            mock_bedrock_client.invoke_model.return_value = self.mock_bedrock_response
            
            # Act
            response = lambda_handler(event, self.mock_context)
            
            # Assert
            self.assertEqual(response["statusCode"], 200)
            response_body = json.loads(response["body"])
            self.assertEqual(response_body["sign"], "Pisces")  # Feb 29 should be Pisces
    
    def test_year_boundary_zodiac_signs(self):
        """Test zodiac signs that span year boundaries (Capricorn)"""
        # Test cases for Capricorn dates
        capricorn_test_cases = [
            {"name": "Test User", "dob": "25/12/1990"},  # December 25
            {"name": "Test User", "dob": "15/01/1991"},  # January 15
        ]
        
        for test_input in capricorn_test_cases:
            with self.subTest(dob=test_input["dob"]):
                event = {"body": json.dumps(test_input)}
                
                with patch('lambda_function.bedrock_client') as mock_bedrock_client, \
                     patch('lambda_function.config') as mock_config:
                    
                    mock_config.get_project_name.return_value = "Cloud Horoscope"
                    mock_config.get_author_name.return_value = "Test Author"
                    mock_config.get_bedrock_config.return_value = {
                        'model_id': 'anthropic.claude-3-haiku-20240307',
                        'region': 'us-east-1',
                        'max_tokens': 200,
                        'temperature': 0.7
                    }
                    mock_bedrock_client.invoke_model.return_value = self.mock_bedrock_response
                    
                    # Act
                    response = lambda_handler(event, self.mock_context)
                    
                    # Assert
                    self.assertEqual(response["statusCode"], 200)
                    response_body = json.loads(response["body"])
                    self.assertEqual(response_body["sign"], "Capricorn")
    
    @patch('lambda_function.bedrock_client')
    @patch('lambda_function.config')
    def test_bedrock_service_unavailable_error(self, mock_config, mock_bedrock_client):
        """Test handling of Bedrock service unavailable error"""
        # Arrange
        mock_config.get_project_name.return_value = "Cloud Horoscope"
        mock_config.get_author_name.return_value = "Test Author"
        mock_config.get_bedrock_config.return_value = {
            'model_id': 'anthropic.claude-3-haiku-20240307',
            'region': 'us-east-1',
            'max_tokens': 200,
            'temperature': 0.7
        }
        
        from botocore.exceptions import ClientError
        error_response = {
            'Error': {
                'Code': 'ServiceUnavailableException',
                'Message': 'Service is temporarily unavailable'
            }
        }
        mock_bedrock_client.invoke_model.side_effect = ClientError(error_response, 'InvokeModel')
        
        # Act
        response = lambda_handler(self.base_event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 503)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("AI service temporarily unavailable", response_body["error"])
    
    @patch('lambda_function.bedrock_client')
    @patch('lambda_function.config')
    def test_bedrock_rate_limiting_error(self, mock_config, mock_bedrock_client):
        """Test handling of Bedrock rate limiting error"""
        # Arrange
        mock_config.get_project_name.return_value = "Cloud Horoscope"
        mock_config.get_author_name.return_value = "Test Author"
        mock_config.get_bedrock_config.return_value = {
            'model_id': 'anthropic.claude-3-haiku-20240307',
            'region': 'us-east-1',
            'max_tokens': 200,
            'temperature': 0.7
        }
        
        from botocore.exceptions import ClientError
        error_response = {
            'Error': {
                'Code': 'ThrottlingException',
                'Message': 'Rate exceeded'
            }
        }
        mock_bedrock_client.invoke_model.side_effect = ClientError(error_response, 'InvokeModel')
        
        # Act
        response = lambda_handler(self.base_event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 429)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Too many requests", response_body["error"])
    
    @patch('lambda_function.bedrock_client')
    @patch('lambda_function.config')
    def test_bedrock_model_error(self, mock_config, mock_bedrock_client):
        """Test handling of Bedrock model error"""
        # Arrange
        mock_config.get_project_name.return_value = "Cloud Horoscope"
        mock_config.get_author_name.return_value = "Test Author"
        mock_config.get_bedrock_config.return_value = {
            'model_id': 'anthropic.claude-3-haiku-20240307',
            'region': 'us-east-1',
            'max_tokens': 200,
            'temperature': 0.7
        }
        
        from botocore.exceptions import ClientError
        error_response = {
            'Error': {
                'Code': 'ModelNotReadyException',
                'Message': 'Model is not ready'
            }
        }
        mock_bedrock_client.invoke_model.side_effect = ClientError(error_response, 'InvokeModel')
        
        # Act
        response = lambda_handler(self.base_event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 503)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("AI service temporarily unavailable", response_body["error"])
    
    @patch('lambda_function.bedrock_client')
    @patch('lambda_function.config')
    def test_unexpected_system_error(self, mock_config, mock_bedrock_client):
        """Test handling of unexpected system errors"""
        # Arrange
        mock_config.get_project_name.return_value = "Cloud Horoscope"
        mock_config.get_author_name.return_value = "Test Author"
        mock_config.get_bedrock_config.return_value = {
            'model_id': 'anthropic.claude-3-haiku-20240307',
            'region': 'us-east-1',
            'max_tokens': 200,
            'temperature': 0.7
        }
        mock_bedrock_client.invoke_model.side_effect = RuntimeError("Unexpected error")
        
        # Act
        response = lambda_handler(self.base_event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 500)
        response_body = json.loads(response["body"])
        self.assertIn("error", response_body)
        self.assertIn("Internal server error", response_body["error"])
    
    def test_response_includes_cors_headers(self):
        """Test that all responses include proper CORS headers"""
        # Test successful response
        with patch('lambda_function.bedrock_client') as mock_bedrock_client, \
             patch('lambda_function.config') as mock_config:
            
            mock_config.get_project_name.return_value = "Cloud Horoscope"
            mock_config.get_author_name.return_value = "Test Author"
            mock_config.get_bedrock_config.return_value = {
                'model_id': 'anthropic.claude-3-haiku-20240307',
                'region': 'us-east-1',
                'max_tokens': 200,
                'temperature': 0.7
            }
            mock_bedrock_client.invoke_model.return_value = self.mock_bedrock_response
            
            response = lambda_handler(self.base_event, self.mock_context)
            
            self.assertIn("Access-Control-Allow-Origin", response["headers"])
            self.assertEqual(response["headers"]["Access-Control-Allow-Origin"], "*")
        
        # Test error response
        invalid_event = {"body": "invalid json"}
        response = lambda_handler(invalid_event, self.mock_context)
        
        self.assertIn("Access-Control-Allow-Origin", response["headers"])
        self.assertEqual(response["headers"]["Access-Control-Allow-Origin"], "*")
    
    def test_response_includes_request_id_in_errors(self):
        """Test that error responses include request ID for debugging"""
        # Arrange
        invalid_event = {"body": "invalid json"}
        
        # Act
        response = lambda_handler(invalid_event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("request_id", response_body)
        self.assertEqual(response_body["request_id"], "test-request-id-12345")
    
    def test_response_includes_timestamp_in_errors(self):
        """Test that error responses include timestamp"""
        # Arrange
        invalid_event = {"body": "invalid json"}
        
        # Act
        response = lambda_handler(invalid_event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        response_body = json.loads(response["body"])
        self.assertIn("timestamp", response_body)
        
        # Verify timestamp format (ISO format)
        timestamp = response_body["timestamp"]
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            self.fail(f"Timestamp {timestamp} is not in valid ISO format")
    
    @patch('lambda_function.bedrock_client')
    @patch('lambda_function.config')
    def test_all_zodiac_signs_end_to_end(self, mock_config, mock_bedrock_client):
        """Test end-to-end processing for all zodiac signs"""
        # Arrange
        mock_config.get_project_name.return_value = "Cloud Horoscope"
        mock_config.get_author_name.return_value = "Test Author"
        mock_config.get_bedrock_config.return_value = {
            'model_id': 'anthropic.claude-3-haiku-20240307',
            'region': 'us-east-1',
            'max_tokens': 200,
            'temperature': 0.7
        }
        mock_bedrock_client.invoke_model.return_value = self.mock_bedrock_response
        
        # Test cases for each zodiac sign
        zodiac_test_cases = [
            ("25/03/1990", "Aries"),
            ("25/04/1990", "Taurus"),
            ("25/05/1990", "Gemini"),
            ("25/06/1990", "Cancer"),
            ("25/07/1990", "Leo"),
            ("25/08/1990", "Virgo"),
            ("25/09/1990", "Libra"),
            ("25/10/1990", "Scorpio"),
            ("25/11/1990", "Sagittarius"),
            ("25/12/1990", "Capricorn"),
            ("25/01/1990", "Aquarius"),
            ("25/02/1990", "Pisces"),
        ]
        
        for dob, expected_sign in zodiac_test_cases:
            with self.subTest(dob=dob, expected_sign=expected_sign):
                # Arrange
                test_input = {"name": "Test User", "dob": dob}
                event = {"body": json.dumps(test_input)}
                
                # Act
                response = lambda_handler(event, self.mock_context)
                
                # Assert
                self.assertEqual(response["statusCode"], 200)
                response_body = json.loads(response["body"])
                self.assertEqual(response_body["sign"], expected_sign)
                self.assertIn("horoscope", response_body)
                self.assertIn("project", response_body)
                self.assertIn("author", response_body)
    
    @patch('lambda_function.bedrock_client')
    @patch('lambda_function.config')
    def test_environment_variable_integration(self, mock_config, mock_bedrock_client):
        """Test integration with environment variables for project and author names"""
        # Arrange
        mock_config.get_project_name.return_value = "Custom Project Name"
        mock_config.get_author_name.return_value = "Custom Author Name"
        mock_config.get_bedrock_config.return_value = {
            'model_id': 'anthropic.claude-3-haiku-20240307',
            'region': 'us-east-1',
            'max_tokens': 200,
            'temperature': 0.7
        }
        mock_bedrock_client.invoke_model.return_value = self.mock_bedrock_response
        
        # Act
        response = lambda_handler(self.base_event, self.mock_context)
        
        # Assert
        self.assertEqual(response["statusCode"], 200)
        response_body = json.loads(response["body"])
        self.assertEqual(response_body["project"], "Custom Project Name")
        self.assertEqual(response_body["author"], "Custom Author Name")
        
        # Verify config methods were called
        mock_config.get_project_name.assert_called_once()
        mock_config.get_author_name.assert_called_once()


if __name__ == '__main__':
    unittest.main()