"""
CloudHoroscopeFunction - Final working version with Bedrock + Fallback
"""

import json
import logging
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

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Main Lambda handler entry point"""
    logger.info(f"Processing request - Request ID: {context.aws_request_id if context else 'unknown'}")
    
    try:
        # Extract request body
        event_body = event.get('body', '{}')
        if event_body is None:
            event_body = '{}'
        
        # Validate input
        validated_input = validate_input(event_body)
        name = validated_input['name']
        dob = validated_input['dob']
        
        # Calculate zodiac sign
        day, month = parse_date(dob)
        zodiac_sign = get_zodiac_sign(day, month)
        
        logger.info(f"Generating horoscope for {name} ({zodiac_sign})")
        
        # Try Bedrock first, fallback to pre-written horoscopes
        try:
            horoscope = generate_bedrock_horoscope(name, zodiac_sign)
            logger.info("Successfully generated Bedrock horoscope")
        except Exception as e:
            logger.warning(f"Bedrock failed: {str(e)}, using fallback horoscope")
            horoscope = generate_fallback_horoscope(name, zodiac_sign)
        
        # Return success response
        return format_success_response(
            project="Cloud Horoscope",
            author="AWS Developer",
            sign=zodiac_sign,
            horoscope=horoscope
        )
        
    except ValueError as e:
        logger.warning(f"Input validation error: {str(e)}")
        return format_error_response(str(e), 400, context)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return format_error_response("Internal server error. Please try again.", 500, context)

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
    
    raise ValueError(f"Unable to determine zodiac sign for {day}/{month}")

def generate_bedrock_horoscope(name: str, zodiac_sign: str) -> str:
    """Try to generate horoscope using Bedrock"""
    import boto3
    from botocore.exceptions import ClientError
    
    # Try different model IDs and regions
    model_ids = [
        'anthropic.claude-3-haiku-20240307-v1:0',
        'anthropic.claude-3-5-haiku-20241022-v1:0',
        'anthropic.claude-v2:1'
    ]
    
    regions = ['us-east-1', 'us-west-2']
    
    for region in regions:
        for model_id in model_ids:
            try:
                bedrock_client = boto3.client('bedrock-runtime', region_name=region)
                
                request_body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 200,
                    "temperature": 0.7,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Generate a short, fun, AWS-themed horoscope for {name}, a {zodiac_sign}. Mention AWS services humorously. Keep it under 150 words."
                        }
                    ]
                }
                
                response = bedrock_client.invoke_model(
                    modelId=model_id,
                    contentType="application/json",
                    accept="application/json",
                    body=json.dumps(request_body)
                )
                
                response_body = json.loads(response['body'].read())
                
                if 'content' in response_body and len(response_body['content']) > 0:
                    return response_body['content'][0]['text'].strip()
                    
            except Exception as e:
                logger.info(f"Model {model_id} in {region} failed: {str(e)}")
                continue
    
    # If all attempts fail, raise exception to trigger fallback
    raise Exception("All Bedrock attempts failed")

def generate_fallback_horoscope(name: str, zodiac_sign: str) -> str:
    """Generate fallback horoscope when Bedrock is not available"""
    horoscopes = {
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
    
    return horoscopes.get(zodiac_sign, f"The cloud spirits are mysterious today, {name}! Your {zodiac_sign} energy brings unique power to your AWS infrastructure. Trust in your technical intuition and let your services scale naturally.")

def parse_date(dob_string: str) -> tuple:
    """Parse date of birth string and return day and month"""
    try:
        parsed_date = datetime.strptime(dob_string, "%d/%m/%Y")
        return parsed_date.day, parsed_date.month
    except ValueError:
        raise ValueError("Invalid date format. Please use dd/mm/yyyy.")

def validate_input(event_body: str) -> Dict[str, str]:
    """Validate and parse input from API Gateway event"""
    try:
        data = json.loads(event_body)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in request body")
    
    if not isinstance(data, dict):
        raise ValueError("Invalid JSON format in request body")
    
    if "name" not in data:
        raise ValueError("Missing required field: name")
    if "dob" not in data:
        raise ValueError("Missing required field: dob")
    
    name = data["name"]
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name must be a non-empty string")
    if len(name.strip()) > 100:
        raise ValueError("Name must be between 1 and 100 characters")
    
    dob = data["dob"]
    if not isinstance(dob, str):
        raise ValueError("Date of birth must be a string")
    
    return {"name": name.strip(), "dob": dob}

def format_success_response(project: str, author: str, sign: str, horoscope: str) -> Dict[str, Any]:
    """Format successful response for API Gateway"""
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
    """Format error response for API Gateway"""
    error_body = {
        "error": message,
        "timestamp": datetime.now().isoformat()
    }
    
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