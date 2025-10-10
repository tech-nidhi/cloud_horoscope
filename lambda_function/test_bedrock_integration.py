"""
Unit tests for Bedrock integration functionality
"""

import json
import unittest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError, BotoCoreError

from lambda_function import (
    generate_horoscope,
    generate_horoscope_with_retry,
    _generate_horoscope_single_attempt,
    _is_retryable_error,
    get_bedrock_client
)


class TestBedrockIntegration(unittest.TestCase):
    """Test cases for Bedrock integration functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_name = "Alice"
        self.test_zodiac_sign = "Libra"
        self.test_horoscope = "Your Lambda functions are aligned with the stars today, Alice!"
        
        # Mock successful Bedrock response
        self.mock_success_response = {
            'body': Mock(),
            'ResponseMetadata': {'HTTPStatusCode': 200}
        }
        
        # Mock response body content
        self.mock_response_body = {
            'content': [
                {
                    'text': self.test_horoscope,
                    'type': 'text'
                }
            ],
            'id': 'msg_test123',
            'model': 'claude-3-haiku-20240307',
            'role': 'assistant',
            'stop_reason': 'end_turn',
            'stop_sequence': None,
            'type': 'message',
            'usage': {'input_tokens': 50, 'output_tokens': 25}
        }
        
        # Configure mock response body
        self.mock_success_response['body'].read.return_value = json.dumps(self.mock_response_body).encode()

    @patch('lambda_function.bedrock_client')
    def test_generate_horoscope_single_attempt_success(self, mock_client):
        """Test successful single attempt horoscope generation"""
        # Arrange
        mock_client.invoke_model.return_value = self.mock_success_response
        
        # Act
        result = _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        # Assert
        self.assertEqual(result, self.test_horoscope)
        mock_client.invoke_model.assert_called_once()
        
        # Verify the call arguments
        call_args = mock_client.invoke_model.call_args
        self.assertEqual(call_args[1]['modelId'], 'anthropic.claude-3-haiku-20240307')
        self.assertEqual(call_args[1]['contentType'], 'application/json')
        self.assertEqual(call_args[1]['accept'], 'application/json')
        
        # Verify request body structure
        request_body = json.loads(call_args[1]['body'])
        self.assertEqual(request_body['anthropic_version'], 'bedrock-2023-05-31')
        self.assertEqual(request_body['max_tokens'], 200)
        self.assertEqual(request_body['temperature'], 0.7)
        self.assertEqual(len(request_body['messages']), 1)
        self.assertEqual(request_body['messages'][0]['role'], 'user')
        self.assertIn(self.test_name, request_body['messages'][0]['content'])
        self.assertIn(self.test_zodiac_sign, request_body['messages'][0]['content'])

    @patch('lambda_function.bedrock_client')
    def test_generate_horoscope_single_attempt_empty_content(self, mock_client):
        """Test handling of empty content response"""
        # Arrange
        empty_response_body = {
            'content': [],
            'id': 'msg_test123',
            'model': 'claude-3-haiku-20240307'
        }
        mock_response = {
            'body': Mock(),
            'ResponseMetadata': {'HTTPStatusCode': 200}
        }
        mock_response['body'].read.return_value = json.dumps(empty_response_body).encode()
        mock_client.invoke_model.return_value = mock_response
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        self.assertIn("No content received from Bedrock model", str(context.exception))

    @patch('lambda_function.bedrock_client')
    def test_generate_horoscope_single_attempt_missing_content_key(self, mock_client):
        """Test handling of response missing content key"""
        # Arrange
        invalid_response_body = {
            'id': 'msg_test123',
            'model': 'claude-3-haiku-20240307'
            # Missing 'content' key
        }
        mock_response = {
            'body': Mock(),
            'ResponseMetadata': {'HTTPStatusCode': 200}
        }
        mock_response['body'].read.return_value = json.dumps(invalid_response_body).encode()
        mock_client.invoke_model.return_value = mock_response
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        self.assertIn("No content received from Bedrock model", str(context.exception))

    @patch('lambda_function.bedrock_client')
    def test_generate_horoscope_single_attempt_throttling_error(self, mock_client):
        """Test handling of throttling exception"""
        # Arrange
        error_response = {
            'Error': {
                'Code': 'ThrottlingException',
                'Message': 'Rate exceeded'
            }
        }
        mock_client.invoke_model.side_effect = ClientError(error_response, 'InvokeModel')
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        self.assertIn("Rate limiting error", str(context.exception))

    @patch('lambda_function.bedrock_client')
    def test_generate_horoscope_single_attempt_service_unavailable_error(self, mock_client):
        """Test handling of service unavailable exception"""
        # Arrange
        error_response = {
            'Error': {
                'Code': 'ServiceUnavailableException',
                'Message': 'Service temporarily unavailable'
            }
        }
        mock_client.invoke_model.side_effect = ClientError(error_response, 'InvokeModel')
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        self.assertIn("Service unavailable", str(context.exception))

    @patch('lambda_function.bedrock_client')
    def test_generate_horoscope_single_attempt_model_not_ready_error(self, mock_client):
        """Test handling of model not ready exception"""
        # Arrange
        error_response = {
            'Error': {
                'Code': 'ModelNotReadyException',
                'Message': 'Model is not ready'
            }
        }
        mock_client.invoke_model.side_effect = ClientError(error_response, 'InvokeModel')
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        self.assertIn("Model not ready", str(context.exception))

    @patch('lambda_function.bedrock_client')
    def test_generate_horoscope_single_attempt_validation_error(self, mock_client):
        """Test handling of validation exception"""
        # Arrange
        error_response = {
            'Error': {
                'Code': 'ValidationException',
                'Message': 'Invalid request parameters'
            }
        }
        mock_client.invoke_model.side_effect = ClientError(error_response, 'InvokeModel')
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        self.assertIn("Validation error", str(context.exception))

    @patch('lambda_function.bedrock_client')
    def test_generate_horoscope_single_attempt_generic_client_error(self, mock_client):
        """Test handling of generic client error"""
        # Arrange
        error_response = {
            'Error': {
                'Code': 'UnknownException',
                'Message': 'Unknown error occurred'
            }
        }
        mock_client.invoke_model.side_effect = ClientError(error_response, 'InvokeModel')
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        self.assertIn("Bedrock client error", str(context.exception))

    @patch('lambda_function.bedrock_client')
    def test_generate_horoscope_single_attempt_botocore_error(self, mock_client):
        """Test handling of BotoCoreError"""
        # Arrange
        mock_client.invoke_model.side_effect = BotoCoreError()
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        self.assertIn("Bedrock connection error", str(context.exception))

    @patch('lambda_function.bedrock_client')
    def test_generate_horoscope_single_attempt_json_decode_error(self, mock_client):
        """Test handling of JSON decode error"""
        # Arrange
        mock_response = {
            'body': Mock(),
            'ResponseMetadata': {'HTTPStatusCode': 200}
        }
        mock_response['body'].read.return_value = b'invalid json'
        mock_client.invoke_model.return_value = mock_response
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        self.assertIn("Response parsing error", str(context.exception))

    def test_is_retryable_error_throttling(self):
        """Test retryable error detection for throttling"""
        error = Exception("Rate limiting error: Too many requests")
        self.assertTrue(_is_retryable_error(error))

    def test_is_retryable_error_service_unavailable(self):
        """Test retryable error detection for service unavailable"""
        error = Exception("Service unavailable: Temporary outage")
        self.assertTrue(_is_retryable_error(error))

    def test_is_retryable_error_connection_error(self):
        """Test retryable error detection for connection error"""
        error = Exception("Bedrock connection error: Network timeout")
        self.assertTrue(_is_retryable_error(error))

    def test_is_retryable_error_model_not_ready(self):
        """Test retryable error detection for model not ready"""
        error = Exception("Model not ready: Please try again")
        self.assertTrue(_is_retryable_error(error))

    def test_is_retryable_error_non_retryable(self):
        """Test non-retryable error detection"""
        error = Exception("Validation error: Invalid input")
        self.assertFalse(_is_retryable_error(error))

    @patch('lambda_function._generate_horoscope_single_attempt')
    def test_generate_horoscope_with_retry_success_first_attempt(self, mock_single_attempt):
        """Test successful generation on first attempt"""
        # Arrange
        mock_single_attempt.return_value = self.test_horoscope
        
        # Act
        result = generate_horoscope_with_retry(self.test_name, self.test_zodiac_sign)
        
        # Assert
        self.assertEqual(result, self.test_horoscope)
        mock_single_attempt.assert_called_once_with(self.test_name, self.test_zodiac_sign)

    @patch('lambda_function._generate_horoscope_single_attempt')
    @patch('time.sleep')
    def test_generate_horoscope_with_retry_success_after_retries(self, mock_sleep, mock_single_attempt):
        """Test successful generation after retries"""
        # Arrange
        retryable_error = Exception("Rate limiting error: Too many requests")
        mock_single_attempt.side_effect = [
            retryable_error,  # First attempt fails
            retryable_error,  # Second attempt fails
            self.test_horoscope  # Third attempt succeeds
        ]
        
        # Act
        result = generate_horoscope_with_retry(self.test_name, self.test_zodiac_sign)
        
        # Assert
        self.assertEqual(result, self.test_horoscope)
        self.assertEqual(mock_single_attempt.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
        
        # Verify exponential backoff
        mock_sleep.assert_any_call(1)  # 2^0 = 1
        mock_sleep.assert_any_call(2)  # 2^1 = 2

    @patch('lambda_function._generate_horoscope_single_attempt')
    @patch('time.sleep')
    def test_generate_horoscope_with_retry_max_retries_exceeded(self, mock_sleep, mock_single_attempt):
        """Test failure after max retries exceeded"""
        # Arrange
        retryable_error = Exception("Service unavailable: Temporary outage")
        mock_single_attempt.side_effect = retryable_error
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            generate_horoscope_with_retry(self.test_name, self.test_zodiac_sign, max_retries=2)
        
        self.assertEqual(str(context.exception), str(retryable_error))
        self.assertEqual(mock_single_attempt.call_count, 3)  # Initial + 2 retries
        self.assertEqual(mock_sleep.call_count, 2)

    @patch('lambda_function._generate_horoscope_single_attempt')
    def test_generate_horoscope_with_retry_non_retryable_error(self, mock_single_attempt):
        """Test immediate failure for non-retryable error"""
        # Arrange
        non_retryable_error = Exception("Validation error: Invalid input")
        mock_single_attempt.side_effect = non_retryable_error
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            generate_horoscope_with_retry(self.test_name, self.test_zodiac_sign)
        
        self.assertEqual(str(context.exception), str(non_retryable_error))
        mock_single_attempt.assert_called_once()

    @patch('lambda_function.generate_horoscope_with_retry')
    def test_generate_horoscope_public_interface(self, mock_retry_function):
        """Test public generate_horoscope function"""
        # Arrange
        mock_retry_function.return_value = self.test_horoscope
        
        # Act
        result = generate_horoscope(self.test_name, self.test_zodiac_sign)
        
        # Assert
        self.assertEqual(result, self.test_horoscope)
        mock_retry_function.assert_called_once_with(self.test_name, self.test_zodiac_sign)

    @patch('lambda_function.config')
    @patch('boto3.client')
    def test_get_bedrock_client_initialization(self, mock_boto3_client, mock_config):
        """Test Bedrock client initialization"""
        # Arrange
        mock_config.get_bedrock_config.return_value = {
            'region': 'us-west-2',
            'model_id': 'anthropic.claude-3-haiku-20240307'
        }
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client
        
        # Act
        result = get_bedrock_client()
        
        # Assert
        self.assertEqual(result, mock_client)
        mock_boto3_client.assert_called_once_with(
            'bedrock-runtime',
            region_name='us-west-2'
        )

    @patch('lambda_function.bedrock_client')
    def test_prompt_template_formatting(self, mock_client):
        """Test that prompt template is correctly formatted"""
        # Arrange
        mock_client.invoke_model.return_value = self.mock_success_response
        test_name = "TestUser"
        test_sign = "Gemini"
        
        # Act
        _generate_horoscope_single_attempt(test_name, test_sign)
        
        # Assert
        call_args = mock_client.invoke_model.call_args
        request_body = json.loads(call_args[1]['body'])
        prompt = request_body['messages'][0]['content']
        
        # Verify prompt contains expected elements
        self.assertIn("witty cloud astrologer", prompt)
        self.assertIn(test_name, prompt)
        self.assertIn(test_sign, prompt)
        self.assertIn("AWS services", prompt)
        self.assertIn("Lambda, EC2, S3, CloudFront", prompt)

    @patch('lambda_function.bedrock_client')
    def test_response_text_stripping(self, mock_client):
        """Test that response text is properly stripped of whitespace"""
        # Arrange
        horoscope_with_whitespace = "  \n  Your stars are aligned!  \n  "
        response_body = {
            'content': [{'text': horoscope_with_whitespace, 'type': 'text'}]
        }
        mock_response = {
            'body': Mock(),
            'ResponseMetadata': {'HTTPStatusCode': 200}
        }
        mock_response['body'].read.return_value = json.dumps(response_body).encode()
        mock_client.invoke_model.return_value = mock_response
        
        # Act
        result = _generate_horoscope_single_attempt(self.test_name, self.test_zodiac_sign)
        
        # Assert
        self.assertEqual(result, "Your stars are aligned!")


if __name__ == '__main__':
    unittest.main()