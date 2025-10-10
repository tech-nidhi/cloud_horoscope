"""
CloudHoroscopeFunction - AWS Lambda function for generating cloud-themed horoscopes
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional

import boto3
from botocore.exceptions import ClientError, BotoCoreError

# Try to import config, use defaults if it fails
try:
    from config import config
except ImportError:
    logger.warning("Config module not found, using default configuration")
    # Create a simple config object with defaults
    class SimpleConfig:
        def get_project_name(self):
            return "Cloud Horoscope"
        def get_author_name(self):
            return "AWS Developer"
        def get_bedrock_config(self):
            return {
                'model_id': 'anthropic.claude-3-haiku-20240307',
                'region': 'us-east-1',
                'max_tokens': 200,
                'temperature': 0.7
            }
    config = SimpleConfig()

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Zodiac date ranges with accurate astronomical dates
# Format: ((start_month, start_day), (end_month, end_day), "Sign Name")
ZODIAC_RANGES = [
    ((3, 21), (4, 19), "Aries"),
    ((4, 20), (5, 20), "Taurus"),
    ((5, 21), (6, 20), "Gemini"),
    ((6, 21), (7, 22), "Cancer"),
    ((7, 23), (8, 22), "Leo"),
    ((8, 23), (9, 22), "Virgo"),
    ((9, 23), (10, 22), "Libra"),
    ((10, 23), (11, 21), "Scorpio"),
    ((11, 22), (12, 21), "Sagittarius"),
    ((12, 22), (1, 19), "Capricorn"),  # Spans year boundary
    ((1, 20), (2, 18), "Aquarius"),
    ((2, 19), (3, 20), "Pisces")
]


# Initialize Bedrock client outside handler for connection reuse
def get_bedrock_client():
    """
    Initialize and return Bedrock Runtime client
    
    Returns:
        boto3 Bedrock Runtime client configured with region from environment
    """
    try:
        bedrock_config = config.get_bedrock_config()
        return boto3.client(
            'bedrock-runtime',
            region_name=bedrock_config['region']
        )
    except Exception as e:
        logger.error(f"Failed to initialize Bedrock client: {str(e)}")
        return None


# Global client instance for connection reuse
bedrock_client = None
try:
    bedrock_client = get_bedrock_client()
except Exception as e:
    logger.error(f"Failed to initialize global Bedrock client: {str(e)}")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler entry point
    
    Args:
        event: API Gateway event containing request data
        context: Lambda context object
        
    Returns:
        API Gateway compatible response
    """
    # Log the incoming request for debugging
    logger.info(f"Processing request - Request ID: {context.aws_request_id if context else 'unknown'}")
    
    try:
        # Extract request body from API Gateway event
        event_body = event.get('body', '{}')
        if event_body is None:
            event_body = '{}'
        
        logger.info("Validating input parameters")
        # Validate and parse input parameters
        validated_input = validate_input(event_body)
        name = validated_input['name']
        dob = validated_input['dob']
        
        logger.info(f"Calculating zodiac sign for date: {dob}")
        # Parse date and calculate zodiac sign
        day, month = parse_date(dob)
        zodiac_sign = get_zodiac_sign(day, month)
        
        logger.info(f"Generating horoscope for {name} ({zodiac_sign})")
        # Generate horoscope using Bedrock AI
        horoscope = generate_horoscope(name, zodiac_sign)
        
        logger.info("Request processed successfully")
        # Format and return success response
        return format_success_response(
            project=config.get_project_name(),
            author=config.get_author_name(),
            sign=zodiac_sign,
            horoscope=horoscope
        )
        
    except ValueError as e:
        # Handle input validation errors
        logger.warning(f"Input validation error: {str(e)}")
        return handle_validation_error(e, context)
        
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        
        # Check if this is a service-related error
        error_message = str(e).lower()
        service_error_indicators = [
            'bedrock', 'rate limiting', 'throttling', 'service unavailable',
            'model not ready', 'timeout', 'connection error'
        ]
        
        if any(indicator in error_message for indicator in service_error_indicators):
            return handle_service_error(e, context)
        else:
            # Handle unexpected system errors
            return handle_system_error(e, context)


def get_zodiac_sign(day: int, month: int) -> str:
    """
    Determine zodiac sign from birth date
    
    Args:
        day: Day of birth (1-31)
        month: Month of birth (1-12)
        
    Returns:
        Zodiac sign name
    """
    # Validate input parameters
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}. Must be between 1 and 12.")
    if not (1 <= day <= 31):
        raise ValueError(f"Invalid day: {day}. Must be between 1 and 31.")
    
    # Check each zodiac range
    for (start_month, start_day), (end_month, end_day), sign in ZODIAC_RANGES:
        # Handle normal ranges (within same year)
        if start_month <= end_month:
            if (month == start_month and day >= start_day) or \
               (month == end_month and day <= end_day) or \
               (start_month < month < end_month):
                return sign
        else:
            # Handle year boundary cases (like Capricorn: Dec 22 - Jan 19)
            if (month == start_month and day >= start_day) or \
               (month == end_month and day <= end_day):
                return sign
    
    # This should never happen with correct ZODIAC_RANGES data
    raise ValueError(f"Unable to determine zodiac sign for {day}/{month}")


def generate_horoscope_with_retry(name: str, zodiac_sign: str, max_retries: int = 3) -> str:
    """
    Generate AI-powered horoscope using Amazon Bedrock with retry logic
    
    Args:
        name: User's name
        zodiac_sign: User's zodiac sign
        max_retries: Maximum number of retry attempts
        
    Returns:
        Generated horoscope text
        
    Raises:
        Exception: If all retry attempts fail
    """
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return _generate_horoscope_single_attempt(name, zodiac_sign)
        except Exception as e:
            last_exception = e
            
            # Check if this is a retryable error
            if _is_retryable_error(e) and attempt < max_retries:
                # Exponential backoff: 1s, 2s, 4s
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            else:
                # Non-retryable error or max retries reached
                break
    
    # All retries failed, raise the last exception
    raise last_exception


def _generate_horoscope_single_attempt(name: str, zodiac_sign: str) -> str:
    """
    Single attempt to generate horoscope via Bedrock API
    
    Args:
        name: User's name
        zodiac_sign: User's zodiac sign
        
    Returns:
        Generated horoscope text
        
    Raises:
        Exception: If Bedrock API call fails
    """
    # Check if client is available
    if bedrock_client is None:
        raise Exception("Bedrock client not initialized")
    
    # Get Bedrock configuration
    bedrock_config = config.get_bedrock_config()
    
    # Create prompt template for Claude 3 Haiku
    prompt_template = (
        "You are a witty cloud astrologer. Generate a short, fun, AWS-themed horoscope "
        "for {name}, born under the {sign} zodiac sign. Mention AWS services humorously "
        "(like Lambda, EC2, S3, CloudFront, etc.). Keep it under 150 words."
    )
    
    prompt = prompt_template.format(name=name, sign=zodiac_sign)
    
    # Format request with proper Anthropic message structure
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": bedrock_config['max_tokens'],
        "temperature": bedrock_config['temperature'],
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        logger.info(f"Calling Bedrock with model: {bedrock_config['model_id']}")
        
        # Call Bedrock API
        response = bedrock_client.invoke_model(
            modelId=bedrock_config['model_id'],
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body)
        )
        
        # Parse response and extract content
        response_body = json.loads(response['body'].read())
        logger.info("Bedrock response received successfully")
        
        # Extract the generated text from Claude's response
        if 'content' in response_body and len(response_body['content']) > 0:
            horoscope_text = response_body['content'][0]['text']
            return horoscope_text.strip()
        else:
            raise Exception("No content received from Bedrock model")
            
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', '')
        error_message = e.response.get('Error', {}).get('Message', str(e))
        logger.error(f"Bedrock ClientError: {error_code} - {error_message}")
        
        # Handle specific AWS service errors
        if error_code == 'AccessDeniedException':
            raise Exception(f"Access denied to Bedrock model. Check IAM permissions: {error_message}")
        elif error_code == 'ThrottlingException':
            raise Exception(f"Rate limiting error: {error_message}")
        elif error_code == 'ServiceUnavailableException':
            raise Exception(f"Service unavailable: {error_message}")
        elif error_code == 'ModelNotReadyException':
            raise Exception(f"Model not ready: {error_message}")
        elif error_code == 'ValidationException':
            raise Exception(f"Validation error: {error_message}")
        else:
            raise Exception(f"Bedrock client error ({error_code}): {error_message}")
            
    except BotoCoreError as e:
        logger.error(f"Bedrock BotoCoreError: {str(e)}")
        raise Exception(f"Bedrock connection error: {str(e)}")
        
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Response parsing error: {str(e)}")
        raise Exception(f"Response parsing error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in Bedrock call: {str(e)}")
        raise Exception(f"Unexpected Bedrock error: {str(e)}")


def _is_retryable_error(error: Exception) -> bool:
    """
    Determine if an error is retryable
    
    Args:
        error: Exception to check
        
    Returns:
        True if error should be retried, False otherwise
    """
    error_message = str(error).lower()
    
    # Retryable conditions
    retryable_patterns = [
        'rate limiting',
        'throttling',
        'service unavailable',
        'connection error',
        'timeout',
        'model not ready'
    ]
    
    return any(pattern in error_message for pattern in retryable_patterns)


def generate_fallback_horoscope(name: str, zodiac_sign: str) -> str:
    """
    Generate a fallback horoscope when Bedrock is not available
    
    Args:
        name: User's name
        zodiac_sign: User's zodiac sign
        
    Returns:
        Pre-written horoscope text
    """
    fallback_horoscopes = {
        "Aries": f"Your Lambda functions are charging ahead today, {name}! Like a true Aries, your EC2 instances will scale with fiery determination. S3 buckets overflow with success, and your CloudWatch metrics show blazing performance. Beware of over-provisioning - even rams need to watch their AWS bill!",
        
        "Taurus": f"Steady and reliable like your favorite EBS volumes, {name}! Your methodical approach to cloud architecture brings stability today. RDS databases respond to your patient queries, while your VPC configurations remain rock-solid. A cost optimization opportunity awaits in your reserved instances.",
        
        "Gemini": f"Your dual nature shines in multi-region deployments today, {name}! Like the twins, your load balancers distribute traffic with perfect harmony. API Gateway calls flow smoothly, and your microservices communicate beautifully. Consider implementing blue-green deployments for extra versatility.",
        
        "Cancer": f"Your protective instincts serve your security groups well today, {name}! Like a caring crab, you shield your resources with perfect IAM policies. CloudTrail logs reveal hidden insights, and your backup strategies provide emotional comfort. Trust your intuition about that suspicious network traffic.",
        
        "Leo": f"Roar with confidence today, {name}! Your Lambda functions command attention like a true king of the cloud. EC2 instances bow to your scaling prowess, and S3 storage basks in your organizational glory. The stars align for a breakthrough in your CloudFormation templates. Avoid over-provisioning - even lions need to watch their AWS bill!",
        
        "Virgo": f"Your attention to detail perfects every CloudFormation template today, {name}! Like a meticulous Virgo, you optimize every resource with precision. Your monitoring dashboards reveal patterns others miss, and your cost analysis brings order to chaos. A small configuration tweak will yield big performance gains.",
        
        "Libra": f"Balance flows through your architecture today, {name}! Your load balancers achieve perfect harmony, while auto-scaling groups maintain ideal equilibrium. API rate limits find their sweet spot, and your multi-AZ deployments create beautiful symmetry. Seek consensus before that major infrastructure change.",
        
        "Scorpio": f"Your penetrating insights uncover hidden security vulnerabilities today, {name}! Like a determined Scorpio, you dive deep into CloudTrail logs and emerge with powerful revelations. Your encryption strategies intensify, and database connections transform mysteriously. Trust your instincts about that anomalous traffic pattern.",
        
        "Sagittarius": f"Adventure calls from distant AWS regions today, {name}! Your global deployments expand horizons like a true Sagittarius archer. CloudFront distributions carry your content to far-off lands, while your wandering spirit discovers new services. Aim high with that ambitious migration project!",
        
        "Capricorn": f"Your methodical approach to cloud architecture reaches new heights today, {name}! Like a mountain goat scaling AWS peaks, your systematic deployment strategies will reach new summits. RDS databases respond to your structured queries, while VPC configurations align perfectly. The stars suggest a cost optimization opportunity in your unused Elastic IPs.",
        
        "Aquarius": f"Innovation flows through your serverless functions today, {name}! Your revolutionary ideas transform traditional architectures, while your humanitarian spirit optimizes costs for everyone. Step Functions orchestrate workflows with Aquarian precision. That experimental service you've been eyeing? Today's the day to try it!",
        
        "Pisces": f"Your Lambda functions are swimming in success today, {name}! The cosmic EC2 currents favor your deployments, while S3 buckets overflow with data treasures. CloudWatch metrics show positive energy flowing through your infrastructure. A mysterious DynamoDB query may reveal hidden insights this afternoon."
    }
    
    return fallback_horoscopes.get(zodiac_sign, f"The cloud spirits are mysterious today, {name}! Your {zodiac_sign} energy brings unique power to your AWS infrastructure. Trust in your technical intuition and let your services scale naturally.")


def generate_horoscope(name: str, zodiac_sign: str) -> str:
    """
    Generate AI-powered horoscope using Amazon Bedrock (public interface)
    
    Args:
        name: User's name
        zodiac_sign: User's zodiac sign
        
    Returns:
        Generated horoscope text
        
    Raises:
        Exception: If horoscope generation fails after retries
    """
    # Check if Bedrock client is available
    if bedrock_client is None:
        logger.warning("Bedrock client not available, using fallback horoscope")
        return generate_fallback_horoscope(name, zodiac_sign)
    
    try:
        return generate_horoscope_with_retry(name, zodiac_sign)
    except Exception as e:
        logger.error(f"Bedrock horoscope generation failed: {str(e)}")
        logger.info("Using fallback horoscope")
        return generate_fallback_horoscope(name, zodiac_sign)


def parse_date(dob_string: str) -> tuple[int, int]:
    """
    Parse date of birth string and return day and month
    
    Args:
        dob_string: Date string in dd/mm/yyyy format
        
    Returns:
        Tuple of (day, month) as integers
        
    Raises:
        ValueError: If date format is invalid or date is invalid
    """
    try:
        # Parse using datetime.strptime with exact format
        parsed_date = datetime.strptime(dob_string, "%d/%m/%Y")
        return parsed_date.day, parsed_date.month
    except ValueError:
        raise ValueError("Invalid date format. Please use dd/mm/yyyy.")


def validate_input(event_body: str) -> Dict[str, str]:
    """
    Validate and parse input from API Gateway event
    
    Args:
        event_body: JSON string from API Gateway
        
    Returns:
        Dictionary with validated name and dob
        
    Raises:
        ValueError: If input validation fails
    """
    try:
        # Parse JSON from event body
        data = json.loads(event_body)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in request body")
    
    # Check if data is a dictionary (not null, array, etc.)
    if not isinstance(data, dict):
        raise ValueError("Invalid JSON format in request body")
    
    # Validate required fields exist
    if "name" not in data:
        raise ValueError("Missing required field: name")
    if "dob" not in data:
        raise ValueError("Missing required field: dob")
    
    # Validate name field
    name = data["name"]
    if not isinstance(name, str):
        raise ValueError("Name must be a string")
    if not name.strip():
        raise ValueError("Name cannot be empty")
    if len(name.strip()) > 100:
        raise ValueError("Name must be between 1 and 100 characters")
    
    # Validate date of birth field
    dob = data["dob"]
    if not isinstance(dob, str):
        raise ValueError("Date of birth must be a string")
    
    # Parse and validate the date format
    try:
        day, month = parse_date(dob)
    except ValueError as e:
        raise ValueError(str(e))
    
    # Return validated data
    return {
        "name": name.strip(),
        "dob": dob
    }


def format_success_response(project: str, author: str, sign: str, horoscope: str) -> Dict[str, Any]:
    """
    Format successful response for API Gateway
    
    Args:
        project: Project name
        author: Author name
        sign: Zodiac sign
        horoscope: Generated horoscope
        
    Returns:
        API Gateway response dictionary
    """
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "project": project,
            "author": author,
            "sign": sign,
            "horoscope": horoscope
        })
    }


def format_error_response(message: str, status_code: int = 400, context: Any = None) -> Dict[str, Any]:
    """
    Format error response for API Gateway
    
    Args:
        message: Error message
        status_code: HTTP status code
        context: Lambda context object for request ID
        
    Returns:
        API Gateway error response dictionary
    """
    error_body = {
        "error": message,
        "timestamp": datetime.now().isoformat()
    }
    
    # Include request ID if context is available
    if context and hasattr(context, 'aws_request_id'):
        error_body["request_id"] = context.aws_request_id
    
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(error_body)
    }


def handle_validation_error(error: ValueError, context: Any = None) -> Dict[str, Any]:
    """
    Handle input validation errors with appropriate status codes
    
    Args:
        error: ValueError from input validation
        context: Lambda context object
        
    Returns:
        API Gateway error response dictionary
    """
    return format_error_response(str(error), 400, context)


def handle_service_error(error: Exception, context: Any = None) -> Dict[str, Any]:
    """
    Handle service-related errors (Bedrock, AWS services)
    
    Args:
        error: Exception from service calls
        context: Lambda context object
        
    Returns:
        API Gateway error response dictionary
    """
    error_message = str(error).lower()
    
    # Determine appropriate status code based on error type
    if 'rate limiting' in error_message or 'throttling' in error_message:
        status_code = 429
        message = "Too many requests. Please try again later."
    elif 'service unavailable' in error_message or 'model not ready' in error_message:
        status_code = 503
        message = "AI service temporarily unavailable. Please try again."
    elif 'timeout' in error_message:
        status_code = 504
        message = "Request timeout. Please try again."
    else:
        status_code = 500
        message = "Error generating horoscope. Please try again."
    
    return format_error_response(message, status_code, context)


def handle_system_error(error: Exception, context: Any = None) -> Dict[str, Any]:
    """
    Handle unexpected system errors
    
    Args:
        error: Unexpected exception
        context: Lambda context object
        
    Returns:
        API Gateway error response dictionary
    """
    return format_error_response(
        "Internal server error. Please try again.",
        500,
        context
    )