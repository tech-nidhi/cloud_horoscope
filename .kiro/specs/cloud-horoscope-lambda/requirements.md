# Requirements Document

## Introduction

The CloudHoroscopeFunction is an AWS Lambda function that generates personalized, cloud-themed horoscopes using Amazon Bedrock AI models. Users provide their name and date of birth, and the system determines their zodiac sign and creates a fun, AWS-themed horoscope message. The function integrates with Amazon Bedrock for AI-powered content generation and returns structured JSON responses compatible with API Gateway.

## Requirements

### Requirement 1

**User Story:** As a user, I want to submit my name and date of birth to receive a personalized cloud-themed horoscope, so that I can enjoy entertaining AWS-themed astrological content.

#### Acceptance Criteria

1. WHEN a user provides a valid JSON input with "name" and "dob" fields THEN the system SHALL accept the request and process it
2. WHEN the "dob" field is in dd/mm/yyyy format THEN the system SHALL parse it using datetime.strptime(dob, "%d/%m/%Y")
3. WHEN the input contains a valid name string THEN the system SHALL use it in the personalized horoscope response
4. WHEN the system processes the request successfully THEN it SHALL return a 200 status code with the horoscope data

### Requirement 2

**User Story:** As a user, I want the system to automatically determine my zodiac sign from my date of birth, so that I receive an accurate astrological reading.

#### Acceptance Criteria

1. WHEN the system receives a valid date of birth THEN it SHALL extract the day and month values
2. WHEN the day and month are extracted THEN the system SHALL call a get_zodiac_sign(day, month) helper function
3. WHEN the zodiac sign is determined THEN it SHALL be included in the response body under the "sign" field
4. WHEN the zodiac calculation is complete THEN it SHALL support all 12 zodiac signs (Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces)

### Requirement 3

**User Story:** As a user, I want to receive AI-generated horoscopes that incorporate AWS services humorously, so that I get entertaining cloud-themed content.

#### Acceptance Criteria

1. WHEN the system needs to generate a horoscope THEN it SHALL use Amazon Bedrock Runtime client via boto3
2. WHEN calling Bedrock THEN it SHALL use the model ID "anthropic.claude-3-haiku-20240307" by default
3. WHEN generating the prompt THEN it SHALL include the template: "You are a witty cloud astrologer. Generate a short, fun, AWS-themed horoscope for {name}, born under the {sign} zodiac sign. Mention AWS services humorously (like Lambda, EC2, S3, CloudFront, etc.)."
4. WHEN the horoscope is generated THEN it SHALL include references to AWS services in a humorous context
5. WHEN the AI response is received THEN it SHALL be included in the response body under the "horoscope" field

### Requirement 4

**User Story:** As a user, I want to receive properly formatted JSON responses, so that I can easily integrate the function with web applications and API Gateway.

#### Acceptance Criteria

1. WHEN the function executes successfully THEN it SHALL return a response with "statusCode": 200
2. WHEN returning a successful response THEN the body SHALL contain "project", "author", "sign", and "horoscope" fields
3. WHEN the response is formatted THEN it SHALL be compatible with AWS API Gateway response format
4. WHEN environment variables are available THEN the system SHALL use PROJECT_NAME for the "project" field (default: "Cloud Horoscope")
5. WHEN environment variables are available THEN the system SHALL use AUTHOR_NAME for the "author" field (default: "Unknown Author")

### Requirement 5

**User Story:** As a user, I want to receive clear error messages when I provide invalid input, so that I can correct my request and try again.

#### Acceptance Criteria

1. WHEN the date of birth format is invalid THEN the system SHALL return a 400 status code
2. WHEN returning an error response THEN the body SHALL contain an "error" field with the message "Invalid date format. Please use dd/mm/yyyy."
3. WHEN the "dob" field is missing THEN the system SHALL handle it gracefully with an appropriate error response
4. WHEN the "name" field is missing THEN the system SHALL handle it gracefully with an appropriate error response
5. WHEN any parsing error occurs THEN the system SHALL not crash and SHALL return a structured error response

### Requirement 6

**User Story:** As a system administrator, I want the Lambda function to have appropriate IAM permissions, so that it can access required AWS services securely with least-privilege access.

#### Acceptance Criteria

1. WHEN the function is deployed THEN it SHALL have permission for bedrock:InvokeModel action
2. WHEN the function is deployed THEN it SHALL have permission for bedrock:InvokeModelWithResponseStream action
3. WHEN the function runs THEN it SHALL have permission for logs:CreateLogGroup action
4. WHEN the function runs THEN it SHALL have permission for logs:CreateLogStream action
5. WHEN the function runs THEN it SHALL have permission for logs:PutLogEvents action
6. WHEN IAM policies are configured THEN they SHALL follow least-privilege principles

### Requirement 7

**User Story:** As a developer, I want the code to be modular and maintainable, so that it can be easily extended and deployed to production.

#### Acceptance Criteria

1. WHEN the code is structured THEN it SHALL use only built-in Python libraries plus boto3
2. WHEN the function is implemented THEN it SHALL have a lambda_handler(event, context) entry point
3. WHEN the zodiac logic is implemented THEN it SHALL be in a separate get_zodiac_sign(day, month) helper function
4. WHEN the code is written THEN it SHALL be clean, readable, and production-ready
5. WHEN environment variables are used THEN they SHALL have sensible defaults for all configurable values