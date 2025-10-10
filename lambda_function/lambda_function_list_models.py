"""
Lambda function to list available Bedrock models
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
    """List available Bedrock models"""
    logger.info(f"Listing Bedrock models - Request ID: {context.aws_request_id if context else 'unknown'}")
    
    try:
        # Get user input for zodiac calculation
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
        # Initialize Bedrock client
        bedrock_client = boto3.client('bedrock', region_name='us-east-1')
        
        # List foundation models
        response = bedrock_client.list_foundation_models()
        
        available_models = []
        claude_models = []
        
        for model in response.get('modelSummaries', []):
            model_info = {
                'modelId': model.get('modelId'),
                'modelName': model.get('modelName'),
                'providerName': model.get('providerName'),
                'inputModalities': model.get('inputModalities', []),
                'outputModalities': model.get('outputModalities', [])
            }
            available_models.append(model_info)
            
            # Filter Claude models
            if 'claude' in model.get('modelId', '').lower():
                claude_models.append(model_info)
        
        logger.info(f"Found {len(available_models)} total models, {len(claude_models)} Claude models")
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "project": "Model Discovery",
                "author": "AWS Developer",
                "sign": zodiac_sign,
                "horoscope": f"🔍 Model Discovery Complete, {name}! Found {len(claude_models)} Claude models: {', '.join([m['modelId'] for m in claude_models[:3]])}. Your {zodiac_sign} energy is perfect for exploring the AI cosmos!",
                "debug_info": {
                    "total_models": len(available_models),
                    "claude_models": claude_models,
                    "all_models": available_models[:10]  # First 10 for brevity
                }
            })
        }
        
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}", exc_info=True)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "project": "Model Discovery",
                "author": "AWS Developer",
                "sign": zodiac_sign if 'zodiac_sign' in locals() else "Scorpio",
                "horoscope": f"🔍 Discovery failed: {str(e)}. But your Lambda functions are persistent like a {zodiac_sign if 'zodiac_sign' in locals() else 'Scorpio'}! Let's try a different approach.",
                "error": str(e)
            })
        }