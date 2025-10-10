# CloudHoroscopeFunction API Examples

This document provides comprehensive examples of request and response formats for the CloudHoroscopeFunction AWS Lambda function.

## Input Format

The function expects a JSON payload with the following structure:

```json
{
  "name": "string (required, 1-100 characters)",
  "dob": "string (required, dd/mm/yyyy format)"
}
```

### Field Specifications

- **name**: User's name (required)
  - Type: String
  - Length: 1-100 characters
  - Cannot be empty or whitespace only
  
- **dob**: Date of birth (required)
  - Type: String
  - Format: dd/mm/yyyy (exact format required)
  - Valid date range: 01/01/1900 to current date
  - Examples: "15/03/1990", "29/02/2000", "01/01/2000"

## Success Response Format

When the request is processed successfully, the function returns:

```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"project\":\"Cloud Horoscope\",\"author\":\"AWS Developer\",\"sign\":\"Pisces\",\"horoscope\":\"Your Lambda functions are aligned perfectly today, dear Pisces! The stars suggest your EC2 instances will scale smoothly, and S3 buckets overflow with good fortune. CloudFront will deliver your dreams at lightning speed. Beware of unexpected API Gateway timeouts around midday.\"}"
}
```

### Success Response Body Fields

- **project**: Project name (from PROJECT_NAME environment variable, default: "Cloud Horoscope")
- **author**: Author name (from AUTHOR_NAME environment variable, default: "Unknown Author")
- **sign**: Calculated zodiac sign based on date of birth
- **horoscope**: AI-generated AWS-themed horoscope text

## Example Requests and Responses

### Example 1: Valid Request - Pisces

**Request:**
```json
{
  "name": "Alice Johnson",
  "dob": "15/03/1990"
}
```

**Response:**
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"project\":\"Cloud Horoscope\",\"author\":\"AWS Developer\",\"sign\":\"Pisces\",\"horoscope\":\"Your Lambda functions are swimming in success today, Alice! The cosmic EC2 currents favor your deployments, while S3 buckets overflow with data treasures. CloudWatch metrics show positive energy flowing through your infrastructure. A mysterious DynamoDB query may reveal hidden insights this afternoon.\"}"
}
```

### Example 2: Valid Request - Leo

**Request:**
```json
{
  "name": "Bob Smith",
  "dob": "01/08/1985"
}
```

**Response:**
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"project\":\"Cloud Horoscope\",\"author\":\"AWS Developer\",\"sign\":\"Leo\",\"horoscope\":\"Roar with confidence today, Bob! Your Lambda functions command attention like a true king of the cloud. EC2 instances bow to your scaling prowess, and S3 storage basks in your organizational glory. The stars align for a breakthrough in your CloudFormation templates. Avoid over-provisioning - even lions need to watch their AWS bill!\"}"
}
```

### Example 3: Valid Request - Capricorn (Year Boundary)

**Request:**
```json
{
  "name": "Carol Davis",
  "dob": "31/12/1995"
}
```

**Response:**
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"project\":\"Cloud Horoscope\",\"author\":\"AWS Developer\",\"sign\":\"Capricorn\",\"horoscope\":\"Your methodical approach to cloud architecture shines today, Carol! Like a mountain goat scaling AWS peaks, your systematic deployment strategies will reach new heights. RDS databases respond to your structured queries, while VPC configurations align perfectly. The stars suggest a cost optimization opportunity in your unused Elastic IPs.\"}"
}
```

### Example 4: Valid Request - Leap Year Date

**Request:**
```json
{
  "name": "David Wilson",
  "dob": "29/02/2000"
}
```

**Response:**
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"project\":\"Cloud Horoscope\",\"author\":\"AWS Developer\",\"sign\":\"Pisces\",\"horoscope\":\"A rare cosmic alignment for a leap year baby, David! Your unique timing brings special powers to your AWS deployments. Lambda functions execute with extraordinary precision, while your S3 lifecycle policies work like magic. The universe whispers secrets about serverless optimization - listen carefully to your CloudWatch logs today.\"}"
}
```

## Error Response Format

All error responses follow this structure:

```json
{
  "statusCode": <HTTP_STATUS_CODE>,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"<ERROR_MESSAGE>\",\"timestamp\":\"<ISO_TIMESTAMP>\",\"request_id\":\"<AWS_REQUEST_ID>\"}"
}
```

## Error Response Examples

### 1. Missing Required Field - Name

**Request:**
```json
{
  "dob": "15/03/1990"
}
```

**Response:**
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Missing required field: name\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 2. Missing Required Field - Date of Birth

**Request:**
```json
{
  "name": "John Doe"
}
```

**Response:**
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Missing required field: dob\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 3. Invalid Date Format

**Request:**
```json
{
  "name": "Jane Doe",
  "dob": "1990-03-15"
}
```

**Response:**
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Invalid date format. Please use dd/mm/yyyy.\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 4. Invalid Date Format - Wrong Separator

**Request:**
```json
{
  "name": "Mike Johnson",
  "dob": "15-03-1990"
}
```

**Response:**
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Invalid date format. Please use dd/mm/yyyy.\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 5. Invalid Date - Non-existent Date

**Request:**
```json
{
  "name": "Sarah Connor",
  "dob": "31/02/1990"
}
```

**Response:**
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Invalid date format. Please use dd/mm/yyyy.\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 6. Empty Name Field

**Request:**
```json
{
  "name": "",
  "dob": "15/03/1990"
}
```

**Response:**
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Name cannot be empty\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 7. Name Too Long

**Request:**
```json
{
  "name": "This is a very long name that exceeds the maximum allowed length of one hundred characters for the name field validation",
  "dob": "15/03/1990"
}
```

**Response:**
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Name must be between 1 and 100 characters\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 8. Invalid JSON Format

**Request:**
```
{
  "name": "John Doe"
  "dob": "15/03/1990"
}
```

**Response:**
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Invalid JSON format in request body\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 9. Non-String Name Field

**Request:**
```json
{
  "name": 12345,
  "dob": "15/03/1990"
}
```

**Response:**
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Name must be a string\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 10. Non-String Date Field

**Request:**
```json
{
  "name": "John Doe",
  "dob": 15031990
}
```

**Response:**
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Date of birth must be a string\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

## Service Error Examples

### 11. Rate Limiting Error

**Response:**
```json
{
  "statusCode": 429,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Too many requests. Please try again later.\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 12. Service Unavailable Error

**Response:**
```json
{
  "statusCode": 503,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"AI service temporarily unavailable. Please try again.\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 13. Request Timeout Error

**Response:**
```json
{
  "statusCode": 504,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Request timeout. Please try again.\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

### 14. Internal Server Error

**Response:**
```json
{
  "statusCode": 500,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"error\":\"Internal server error. Please try again.\",\"timestamp\":\"2024-01-15T10:30:45.123456\",\"request_id\":\"12345678-1234-1234-1234-123456789012\"}"
}
```

## API Gateway Integration

When deployed behind API Gateway, the function expects the input to be in the `body` field of the API Gateway event:

```json
{
  "body": "{\"name\":\"John Doe\",\"dob\":\"15/03/1990\"}",
  "headers": {
    "Content-Type": "application/json"
  },
  "httpMethod": "POST",
  "path": "/horoscope",
  "queryStringParameters": null
}
```

The function automatically extracts the JSON from the `body` field and processes it accordingly.

## Environment Variables

The function uses the following environment variables to customize responses:

- **PROJECT_NAME**: Sets the "project" field in success responses (default: "Cloud Horoscope")
- **AUTHOR_NAME**: Sets the "author" field in success responses (default: "Unknown Author")
- **BEDROCK_MODEL_ID**: Bedrock model to use (default: "anthropic.claude-3-haiku-20240307")
- **BEDROCK_REGION**: AWS region for Bedrock service (default: "us-east-1")
- **BEDROCK_MAX_TOKENS**: Maximum tokens for AI generation (default: 200)
- **BEDROCK_TEMPERATURE**: Temperature for AI creativity (default: 0.7)

## Testing the Function

You can test the function using AWS CLI, AWS Console, or any HTTP client when deployed behind API Gateway:

```bash
# Example using curl with API Gateway endpoint
curl -X POST https://your-api-gateway-url/horoscope \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","dob":"15/03/1990"}'
```

## Zodiac Sign Date Ranges

The function uses the following astronomical date ranges for zodiac sign calculation:

| Zodiac Sign | Date Range |
|-------------|------------|
| Aries | March 21 - April 19 |
| Taurus | April 20 - May 20 |
| Gemini | May 21 - June 20 |
| Cancer | June 21 - July 22 |
| Leo | July 23 - August 22 |
| Virgo | August 23 - September 22 |
| Libra | September 23 - October 22 |
| Scorpio | October 23 - November 21 |
| Sagittarius | November 22 - December 21 |
| Capricorn | December 22 - January 19 |
| Aquarius | January 20 - February 18 |
| Pisces | February 19 - March 20 |

Note: Capricorn spans the year boundary (December to January).