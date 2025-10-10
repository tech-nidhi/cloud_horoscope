"""
Debug version of CloudHoroscopeFunction to identify Bedrock issues
"""

import json
import logging
import boto3
from datetime import datetime
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Zodiac date ranges
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
    ((12, 22), (1, 19), "Capricorn"),
    ((1, 20), (2, 18), "Aquarius"),
    ((2, 19), (3, 20), "Pisces")
]

def get_zodiac_sign(day: int, month: int) -> str:
    """Determine zodiac sign from birth date"""
    for (start_month, start_day), (end_month, end_day), sign in ZODIAC_RANGES:
        if start_month <= end_month:
            if (month == start_month and day >= start_day) or \
               (month == end_month and day <= end_day) or \
               (start_month < month < end_month):
                return sign
        else:
            if (month == start_month and day >= start_day) or \
               (month == end_month and day <= end_day):
                return sign
    
    return "Aquarius"  # Default fallback

def parse_date(dob_string: str) -> tuple:
    """Parse date of birth string and return day and month"""
    try:
        parsed_date = datetime.strptime(dob_string, "%d/%m/%Y")
        return parsed_date.day, parsed_date.month
    except ValueError:
        return 22, 4  # Default to April 22 (Taurus)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Debug Lambda handler"""
    logger.info(f"Debug version - Request ID: {context.aws_request_id if context else 'unknown'}")
    
    try:
        # Test 1: Basic functionality
        logger.info("Test 1: Basic input validation")
        event_body = event.get('body', '{}')
        if event_body is None:
            event_body = '{}'
        
        data = json.loads(event_body)
        name = data.get('name', 'Test User')
        dob = data.get('dob', '22/04/2004')
        
        # Calculate zodiac sign
        day, month = parse_date(dob)
        zodiac_sign = get_zodiac_sign(day, month)
        
        logger.info(f"Input received: name={name}, dob={dob}, zodiac={zodiac_sign}")
        
        # Test 2: Bedrock client initialization
        logger.info("Test 2: Initializing Bedrock client")
        
        # Try different regions
        regions_to_try = ['us-east-1', 'us-west-2', 'eu-west-1']
        bedrock_client = None
        successful_region = None
        
        for region in regions_to_try:
            try:
                logger.info(f"Trying region: {region}")
                bedrock_client = boto3.client('bedrock-runtime', region_name=region)
                successful_region = region
                logger.info(f"Bedrock client initialized successfully in {region}")
                break
            except Exception as e:
                logger.info(f"Region {region} failed: {str(e)}")
                continue
        
        if bedrock_client is None:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({
                    "error": "Bedrock client initialization failed in all regions",
                    "test_stage": "bedrock_client_init"
                })
            }
        
        # Test 3: Simple Bedrock call
        logger.info("Test 3: Testing Bedrock API call")
        try:
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 100,
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "user",
                        "content": "Say hello in one sentence."
                    }
                ]
            }
            
            # Try different model IDs
            model_ids_to_try = [
                # Try the most common working model IDs
                'anthropic.claude-3-haiku-20240307-v1:0',
                'anthropic.claude-3-5-haiku-20241022-v1:0',
                'anthropic.claude-3-sonnet-20240229-v1:0',
                'anthropic.claude-3-5-sonnet-20241022-v1:0',
                'anthropic.claude-v2:1',
                'anthropic.claude-v2',
                'anthropic.claude-instant-v1',
                # Sometimes the model ID is without version
                'anthropic.claude-3-haiku',
                'anthropic.claude-3-sonnet'
            ]
            
            response = None
            successful_model = None
            
            for model_id in model_ids_to_try:
                try:
                    logger.info(f"Trying model: {model_id}")
                    response = bedrock_client.invoke_model(
                        modelId=model_id,
                        contentType="application/json",
                        accept="application/json",
                        body=json.dumps(request_body)
                    )
                    successful_model = model_id
                    logger.info(f"Success with model: {model_id}")
                    break
                except Exception as model_error:
                    logger.info(f"Model {model_id} failed: {str(model_error)}")
                    continue
            
            if response is None:
                raise Exception("No available Bedrock models found")
            
            response_body = json.loads(response['body'].read())
            logger.info("Bedrock API call successful")
            
            if 'content' in response_body and len(response_body['content']) > 0:
                ai_response = response_body['content'][0]['text']
                logger.info(f"AI Response: {ai_response}")
                
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
                    "body": json.dumps({
                        "project": "Cloud Horoscope Debug",
                        "author": "AWS Developer",
                        "sign": zodiac_sign,
                        "horoscope": f"🎉 SUCCESS! Using model {successful_model} in region {successful_region}. AI says: {ai_response}. Your Lambda functions are working perfectly, {name}!"
                    })
                }
            else:
                raise Exception("No content in Bedrock response")
                
        except Exception as e:
            logger.error(f"Bedrock API call failed: {str(e)}")
            
            # Return fallback response with error details
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({
                    "project": "Cloud Horoscope Debug",
                    "author": "AWS Developer", 
                    "sign": zodiac_sign,
                    "horoscope": f"Bedrock failed ({str(e)}), but fallback works! Your Lambda functions are resilient today, {name}! Like a determined {zodiac_sign}, your cloud infrastructure perseveres through challenges."
                })
            }
            
    except Exception as e:
        logger.error(f"General error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "error": f"General error: {str(e)}",
                "test_stage": "general_error"
            })
        }