"""
Comprehensive validation tests for CloudHoroscopeFunction
Tests all acceptance criteria from the requirements document
"""

import json
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add the lambda_function directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lambda_function import (
    lambda_handler, get_zodiac_sign, validate_input, parse_date,
    generate_horoscope, format_success_response, format_error_response,
    handle_validation_error, handle_service_error, handle_system_error
)


class TestRequirement1(unittest.TestCase):
    """
    Test Requirement 1: User input processing
    User Story: As a user, I want to submit my name and date of birth to receive a personalized cloud-themed horoscope
    """
    
    def setUp(self):
        """Set up test environment"""
        self.mock_context = Mock()
        self.mock_context.aws_request_id = "test-request-id"
    
    @patch('lambda_function.generate_horoscope')
    def test_1_1_valid_json_input_accepted(self, mock_generate):
        """
        WHEN a user provides a valid JSON input with "name" and "dob" fields 
        THEN the system SHALL accept the request and process it
        """
        mock_generate.return_value = "Test horoscope"
        
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "15/03/1990"
            })
        }
        
        response = lambda_handler(event, self.mock_context)
        
        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response['body'])
        self.assertIn('horoscope', response_body)
        self.assertIn('sign', response_body)
    
    def test_1_2_date_parsing_ddmmyyyy_format(self):
        """
        WHEN the "dob" field is in dd/mm/yyyy format 
        THEN the system SHALL parse it using datetime.strptime(dob, "%d/%m/%Y")
        """
        # Test valid date parsing
        day, month = parse_date("15/03/1990")
        self.assertEqual(day, 15)
        self.assertEqual(month, 3)
        
        # Test leap year
        day, month = parse_date("29/02/2000")
        self.assertEqual(day, 29)
        self.assertEqual(month, 2)
        
        # Test invalid format should raise ValueError
        with self.assertRaises(ValueError):
            parse_date("1990-03-15")  # Wrong format
        
        with self.assertRaises(ValueError):
            parse_date("15-03-1990")  # Wrong separator
    
    @patch('lambda_function.generate_horoscope')
    def test_1_3_valid_name_used_in_response(self, mock_generate):
        """
        WHEN the input contains a valid name string 
        THEN the system SHALL use it in the personalized horoscope response
        """
        test_name = "Alice Johnson"
        mock_generate.return_value = f"Horoscope for {test_name}"
        
        event = {
            'body': json.dumps({
                "name": test_name,
                "dob": "15/03/1990"
            })
        }
        
        response = lambda_handler(event, self.mock_context)
        
        # Verify the name was passed to generate_horoscope
        mock_generate.assert_called_once()
        args = mock_generate.call_args[0]
        self.assertEqual(args[0], test_name)
    
    @patch('lambda_function.generate_horoscope')
    def test_1_4_successful_processing_returns_200(self, mock_generate):
        """
        WHEN the system processes the request successfully 
        THEN it SHALL return a 200 status code with the horoscope data
        """
        mock_generate.return_value = "Test horoscope"
        
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "15/03/1990"
            })
        }
        
        response = lambda_handler(event, self.mock_context)
        
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('body', response)
        response_body = json.loads(response['body'])
        self.assertIn('horoscope', response_body)


class TestRequirement2(unittest.TestCase):
    """
    Test Requirement 2: Zodiac sign determination
    User Story: As a user, I want the system to automatically determine my zodiac sign from my date of birth
    """
    
    def test_2_1_day_month_extraction(self):
        """
        WHEN the system receives a valid date of birth 
        THEN it SHALL extract the day and month values
        """
        day, month = parse_date("15/03/1990")
        self.assertEqual(day, 15)
        self.assertEqual(month, 3)
        
        day, month = parse_date("01/12/2000")
        self.assertEqual(day, 1)
        self.assertEqual(month, 12)
    
    def test_2_2_zodiac_sign_helper_function_called(self):
        """
        WHEN the day and month are extracted 
        THEN the system SHALL call a get_zodiac_sign(day, month) helper function
        """
        # Test that the function exists and works
        sign = get_zodiac_sign(15, 3)  # March 15 = Pisces
        self.assertEqual(sign, "Pisces")
        
        sign = get_zodiac_sign(21, 3)  # March 21 = Aries
        self.assertEqual(sign, "Aries")
    
    @patch('lambda_function.generate_horoscope')
    def test_2_3_zodiac_sign_in_response(self, mock_generate):
        """
        WHEN the zodiac sign is determined 
        THEN it SHALL be included in the response body under the "sign" field
        """
        mock_generate.return_value = "Test horoscope"
        
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "15/03/1990"  # Pisces
            })
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        response_body = json.loads(response['body'])
        self.assertEqual(response_body['sign'], "Pisces")
    
    def test_2_4_all_12_zodiac_signs_supported(self):
        """
        WHEN the zodiac calculation is complete 
        THEN it SHALL support all 12 zodiac signs
        """
        expected_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        # Test boundary dates for each sign
        test_dates = [
            (21, 3, "Aries"),      # March 21
            (20, 4, "Taurus"),     # April 20
            (21, 5, "Gemini"),     # May 21
            (21, 6, "Cancer"),     # June 21
            (23, 7, "Leo"),        # July 23
            (23, 8, "Virgo"),      # August 23
            (23, 9, "Libra"),      # September 23
            (23, 10, "Scorpio"),   # October 23
            (22, 11, "Sagittarius"), # November 22
            (22, 12, "Capricorn"), # December 22
            (20, 1, "Aquarius"),   # January 20
            (19, 2, "Pisces")      # February 19
        ]
        
        for day, month, expected_sign in test_dates:
            with self.subTest(day=day, month=month):
                sign = get_zodiac_sign(day, month)
                self.assertEqual(sign, expected_sign)
        
        # Verify all expected signs are covered
        calculated_signs = [get_zodiac_sign(day, month) for day, month, _ in test_dates]
        for expected_sign in expected_signs:
            self.assertIn(expected_sign, calculated_signs)


class TestRequirement3(unittest.TestCase):
    """
    Test Requirement 3: AI-generated horoscopes with AWS services
    User Story: As a user, I want to receive AI-generated horoscopes that incorporate AWS services humorously
    """
    
    @patch('lambda_function.bedrock_client')
    def test_3_1_bedrock_runtime_client_used(self, mock_client):
        """
        WHEN the system needs to generate a horoscope 
        THEN it SHALL use Amazon Bedrock Runtime client via boto3
        """
        # Mock the Bedrock response
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'content': [{'text': 'Test horoscope with Lambda and S3'}]
        }).encode()
        mock_client.invoke_model.return_value = mock_response
        
        # Call the function
        horoscope = generate_horoscope("John", "Aries")
        
        # Verify Bedrock client was called
        mock_client.invoke_model.assert_called_once()
        self.assertIsInstance(horoscope, str)
    
    @patch('lambda_function.bedrock_client')
    def test_3_2_correct_model_id_used(self, mock_client):
        """
        WHEN calling Bedrock 
        THEN it SHALL use the model ID "anthropic.claude-3-haiku-20240307" by default
        """
        # Mock the Bedrock response
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'content': [{'text': 'Test horoscope'}]
        }).encode()
        mock_client.invoke_model.return_value = mock_response
        
        # Call the function
        generate_horoscope("John", "Aries")
        
        # Verify correct model ID was used
        call_args = mock_client.invoke_model.call_args
        self.assertEqual(call_args[1]['modelId'], "anthropic.claude-3-haiku-20240307")
    
    @patch('lambda_function.bedrock_client')
    def test_3_3_prompt_template_includes_required_elements(self, mock_client):
        """
        WHEN generating the prompt 
        THEN it SHALL include the specified template with name and sign
        """
        # Mock the Bedrock response
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'content': [{'text': 'Test horoscope'}]
        }).encode()
        mock_client.invoke_model.return_value = mock_response
        
        # Call the function
        generate_horoscope("Alice", "Leo")
        
        # Verify the prompt contains required elements
        call_args = mock_client.invoke_model.call_args
        request_body = json.loads(call_args[1]['body'])
        prompt = request_body['messages'][0]['content']
        
        self.assertIn("Alice", prompt)
        self.assertIn("Leo", prompt)
        self.assertIn("witty cloud astrologer", prompt)
        self.assertIn("AWS-themed horoscope", prompt)
        self.assertIn("AWS services", prompt)
    
    @patch('lambda_function.bedrock_client')
    def test_3_4_aws_services_mentioned_humorously(self, mock_client):
        """
        WHEN the horoscope is generated 
        THEN it SHALL include references to AWS services in a humorous context
        """
        # Mock the Bedrock response with AWS services
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'content': [{'text': 'Your Lambda functions are dancing today! S3 buckets overflow with joy, and EC2 instances smile upon you.'}]
        }).encode()
        mock_client.invoke_model.return_value = mock_response
        
        # Call the function
        horoscope = generate_horoscope("John", "Aries")
        
        # Verify AWS services are mentioned
        aws_services = ["Lambda", "S3", "EC2"]
        for service in aws_services:
            self.assertIn(service, horoscope)
    
    @patch('lambda_function.generate_horoscope')
    def test_3_5_horoscope_field_in_response(self, mock_generate):
        """
        WHEN the AI response is received 
        THEN it SHALL be included in the response body under the "horoscope" field
        """
        test_horoscope = "Your AWS journey shines bright today!"
        mock_generate.return_value = test_horoscope
        
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "15/03/1990"
            })
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        response_body = json.loads(response['body'])
        self.assertEqual(response_body['horoscope'], test_horoscope)


class TestRequirement4(unittest.TestCase):
    """
    Test Requirement 4: Properly formatted JSON responses
    User Story: As a user, I want to receive properly formatted JSON responses for API Gateway integration
    """
    
    @patch('lambda_function.generate_horoscope')
    def test_4_1_successful_response_status_code_200(self, mock_generate):
        """
        WHEN the function executes successfully 
        THEN it SHALL return a response with "statusCode": 200
        """
        mock_generate.return_value = "Test horoscope"
        
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "15/03/1990"
            })
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        self.assertEqual(response['statusCode'], 200)
    
    @patch('lambda_function.generate_horoscope')
    def test_4_2_response_contains_required_fields(self, mock_generate):
        """
        WHEN returning a successful response 
        THEN the body SHALL contain "project", "author", "sign", and "horoscope" fields
        """
        mock_generate.return_value = "Test horoscope"
        
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "15/03/1990"
            })
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        response_body = json.loads(response['body'])
        required_fields = ["project", "author", "sign", "horoscope"]
        
        for field in required_fields:
            self.assertIn(field, response_body)
    
    @patch('lambda_function.generate_horoscope')
    def test_4_3_api_gateway_compatible_format(self, mock_generate):
        """
        WHEN the response is formatted 
        THEN it SHALL be compatible with AWS API Gateway response format
        """
        mock_generate.return_value = "Test horoscope"
        
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "15/03/1990"
            })
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        # Check API Gateway response structure
        self.assertIn('statusCode', response)
        self.assertIn('headers', response)
        self.assertIn('body', response)
        
        # Check headers
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], '*')
        
        # Check body is valid JSON string
        self.assertIsInstance(response['body'], str)
        json.loads(response['body'])  # Should not raise exception
    
    def test_4_4_project_name_from_environment(self):
        """
        WHEN environment variables are available 
        THEN the system SHALL use PROJECT_NAME for the "project" field
        """
        # Test that config module can read environment variables
        from config import Config
        
        # Test with environment variable set
        with patch.dict(os.environ, {'PROJECT_NAME': 'Test Project'}):
            test_config = Config.from_environment()
            self.assertEqual(test_config.get_project_name(), 'Test Project')
        
        # Test default value when environment variable is not set
        with patch.dict(os.environ, {}, clear=True):
            test_config = Config.from_environment()
            self.assertEqual(test_config.get_project_name(), 'Cloud Horoscope')
    
    def test_4_5_author_name_from_environment(self):
        """
        WHEN environment variables are available 
        THEN the system SHALL use AUTHOR_NAME for the "author" field
        """
        # Test that config module can read environment variables
        from config import Config
        
        # Test with environment variable set
        with patch.dict(os.environ, {'AUTHOR_NAME': 'Test Author'}):
            test_config = Config.from_environment()
            self.assertEqual(test_config.get_author_name(), 'Test Author')
        
        # Test default value when environment variable is not set
        with patch.dict(os.environ, {}, clear=True):
            test_config = Config.from_environment()
            self.assertEqual(test_config.get_author_name(), 'Unknown Author')


class TestRequirement5(unittest.TestCase):
    """
    Test Requirement 5: Clear error messages for invalid input
    User Story: As a user, I want to receive clear error messages when I provide invalid input
    """
    
    def test_5_1_invalid_date_format_returns_400(self):
        """
        WHEN the date of birth format is invalid 
        THEN the system SHALL return a 400 status code
        """
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "1990-03-15"  # Wrong format
            })
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        self.assertEqual(response['statusCode'], 400)
    
    def test_5_2_error_response_contains_error_field(self):
        """
        WHEN returning an error response 
        THEN the body SHALL contain an "error" field with appropriate message
        """
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "invalid-date"
            })
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        response_body = json.loads(response['body'])
        self.assertIn('error', response_body)
        self.assertEqual(response_body['error'], "Invalid date format. Please use dd/mm/yyyy.")
    
    def test_5_3_missing_dob_field_handled_gracefully(self):
        """
        WHEN the "dob" field is missing 
        THEN the system SHALL handle it gracefully with an appropriate error response
        """
        event = {
            'body': json.dumps({
                "name": "John Doe"
                # Missing dob field
            })
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        self.assertEqual(response['statusCode'], 400)
        response_body = json.loads(response['body'])
        self.assertEqual(response_body['error'], "Missing required field: dob")
    
    def test_5_4_missing_name_field_handled_gracefully(self):
        """
        WHEN the "name" field is missing 
        THEN the system SHALL handle it gracefully with an appropriate error response
        """
        event = {
            'body': json.dumps({
                "dob": "15/03/1990"
                # Missing name field
            })
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        self.assertEqual(response['statusCode'], 400)
        response_body = json.loads(response['body'])
        self.assertEqual(response_body['error'], "Missing required field: name")
    
    def test_5_5_parsing_errors_return_structured_response(self):
        """
        WHEN any parsing error occurs 
        THEN the system SHALL not crash and SHALL return a structured error response
        """
        # Test invalid JSON
        event = {
            'body': '{"name": "John Doe" "dob": "15/03/1990"}'  # Invalid JSON
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('headers', response)
        self.assertIn('body', response)
        
        response_body = json.loads(response['body'])
        self.assertIn('error', response_body)
        self.assertEqual(response_body['error'], "Invalid JSON format in request body")


class TestRequirement6(unittest.TestCase):
    """
    Test Requirement 6: IAM permissions validation
    User Story: As a system administrator, I want the Lambda function to have appropriate IAM permissions
    """
    
    def test_6_1_to_6_6_iam_policy_document_exists(self):
        """
        Test that IAM policy document exists and contains required permissions
        """
        # Check if IAM policy file exists
        iam_policy_path = os.path.join(os.path.dirname(__file__), 'iam-policy.json')
        self.assertTrue(os.path.exists(iam_policy_path), "IAM policy document should exist")
        
        # Read and validate IAM policy
        with open(iam_policy_path, 'r') as f:
            policy = json.load(f)
        
        # Check policy structure
        self.assertIn('Version', policy)
        self.assertIn('Statement', policy)
        
        # Extract all actions from policy statements
        all_actions = []
        for statement in policy['Statement']:
            if 'Action' in statement:
                actions = statement['Action']
                if isinstance(actions, str):
                    all_actions.append(actions)
                elif isinstance(actions, list):
                    all_actions.extend(actions)
        
        # Required permissions from requirements 6.1-6.6
        required_actions = [
            'bedrock:InvokeModel',
            'bedrock:InvokeModelWithResponseStream',
            'logs:CreateLogGroup',
            'logs:CreateLogStream',
            'logs:PutLogEvents'
        ]
        
        for action in required_actions:
            self.assertIn(action, all_actions, f"Required action {action} should be in IAM policy")


class TestRequirement7(unittest.TestCase):
    """
    Test Requirement 7: Code modularity and maintainability
    User Story: As a developer, I want the code to be modular and maintainable
    """
    
    def test_7_1_only_builtin_and_boto3_dependencies(self):
        """
        WHEN the code is structured 
        THEN it SHALL use only built-in Python libraries plus boto3
        """
        # Check requirements.txt
        requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        self.assertTrue(os.path.exists(requirements_path), "requirements.txt should exist")
        
        with open(requirements_path, 'r') as f:
            requirements = f.read().strip().split('\n')
        
        # Filter out empty lines and comments
        requirements = [req.strip() for req in requirements if req.strip() and not req.strip().startswith('#')]
        
        # Should only contain boto3 (and its dependencies)
        allowed_packages = ['boto3', 'botocore', 'jmespath', 'python-dateutil', 's3transfer', 'six', 'urllib3']
        
        for req in requirements:
            package_name = req.split('==')[0].split('>=')[0].split('<=')[0].strip()
            self.assertIn(package_name, allowed_packages, f"Unexpected dependency: {package_name}")
    
    def test_7_2_lambda_handler_entry_point_exists(self):
        """
        WHEN the function is implemented 
        THEN it SHALL have a lambda_handler(event, context) entry point
        """
        # Import and check lambda_handler function
        from lambda_function import lambda_handler
        
        # Check function signature
        import inspect
        sig = inspect.signature(lambda_handler)
        params = list(sig.parameters.keys())
        
        self.assertEqual(len(params), 2, "lambda_handler should have exactly 2 parameters")
        self.assertEqual(params[0], 'event', "First parameter should be 'event'")
        self.assertEqual(params[1], 'context', "Second parameter should be 'context'")
    
    def test_7_3_separate_zodiac_helper_function(self):
        """
        WHEN the zodiac logic is implemented 
        THEN it SHALL be in a separate get_zodiac_sign(day, month) helper function
        """
        # Import and check get_zodiac_sign function
        from lambda_function import get_zodiac_sign
        
        # Check function signature
        import inspect
        sig = inspect.signature(get_zodiac_sign)
        params = list(sig.parameters.keys())
        
        self.assertEqual(len(params), 2, "get_zodiac_sign should have exactly 2 parameters")
        self.assertEqual(params[0], 'day', "First parameter should be 'day'")
        self.assertEqual(params[1], 'month', "Second parameter should be 'month'")
        
        # Test function works
        result = get_zodiac_sign(15, 3)
        self.assertIsInstance(result, str)
        self.assertIn(result, [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ])
    
    def test_7_4_clean_readable_production_ready_code(self):
        """
        WHEN the code is written 
        THEN it SHALL be clean, readable, and production-ready
        """
        # Check that main functions exist and are documented
        from lambda_function import (
            lambda_handler, get_zodiac_sign, validate_input, 
            parse_date, generate_horoscope
        )
        
        functions_to_check = [
            lambda_handler, get_zodiac_sign, validate_input, 
            parse_date, generate_horoscope
        ]
        
        for func in functions_to_check:
            # Check function has docstring
            self.assertIsNotNone(func.__doc__, f"Function {func.__name__} should have docstring")
            self.assertTrue(len(func.__doc__.strip()) > 0, f"Function {func.__name__} should have non-empty docstring")
    
    def test_7_5_environment_variables_have_defaults(self):
        """
        WHEN environment variables are used 
        THEN they SHALL have sensible defaults for all configurable values
        """
        # Test config module provides defaults
        from config import config
        
        # Test that config methods work without environment variables
        project_name = config.get_project_name()
        author_name = config.get_author_name()
        bedrock_config = config.get_bedrock_config()
        
        self.assertIsInstance(project_name, str)
        self.assertIsInstance(author_name, str)
        self.assertIsInstance(bedrock_config, dict)
        
        # Check bedrock config has required keys
        required_keys = ['model_id', 'region', 'max_tokens', 'temperature']
        for key in required_keys:
            self.assertIn(key, bedrock_config)


class TestAPIGatewayCompatibility(unittest.TestCase):
    """
    Test API Gateway compatibility as specified in task 8.2
    """
    
    @patch('lambda_function.generate_horoscope')
    def test_api_gateway_event_structure(self, mock_generate):
        """Test that function works with API Gateway event structure"""
        mock_generate.return_value = "Test horoscope"
        
        # Simulate API Gateway event
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "15/03/1990"
            }),
            'headers': {
                'Content-Type': 'application/json'
            },
            'httpMethod': 'POST',
            'path': '/horoscope',
            'queryStringParameters': None
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        # Verify API Gateway compatible response
        self.assertIn('statusCode', response)
        self.assertIn('headers', response)
        self.assertIn('body', response)
        self.assertEqual(response['statusCode'], 200)
    
    @patch('lambda_function.generate_horoscope')
    def test_cors_headers_present(self, mock_generate):
        """Test that CORS headers are present for web integration"""
        mock_generate.return_value = "Test horoscope"
        
        event = {
            'body': json.dumps({
                "name": "John Doe",
                "dob": "15/03/1990"
            })
        }
        
        mock_context = Mock()
        mock_context.aws_request_id = "test-request-id"
        
        response = lambda_handler(event, mock_context)
        
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], '*')
        self.assertEqual(response['headers']['Content-Type'], 'application/json')


def run_all_tests():
    """Run all requirement validation tests"""
    print("Running comprehensive requirements validation tests...")
    print("=" * 60)
    
    # Create test suite
    test_classes = [
        TestRequirement1,
        TestRequirement2, 
        TestRequirement3,
        TestRequirement4,
        TestRequirement5,
        TestRequirement6,
        TestRequirement7,
        TestAPIGatewayCompatibility
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall result: {'PASS' if success else 'FAIL'}")
    
    return success


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)