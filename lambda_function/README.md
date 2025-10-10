# CloudHoroscopeFunction Lambda

AWS Lambda function that generates personalized, cloud-themed horoscopes using Amazon Bedrock AI models.

## Project Structure

```
lambda_function/
├── lambda_function.py    # Main Lambda handler and core functions
├── config.py            # Environment configuration handler
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Environment Variables

The following environment variables can be configured:

### Required
- None (all have sensible defaults)

### Optional
- `PROJECT_NAME` - Project name for response (default: "Cloud Horoscope")
- `AUTHOR_NAME` - Author name for response (default: "Unknown Author")
- `DEFAULT_MESSAGE` - Default welcome message (default: "Welcome to Cloud Horoscope powered by AWS!")
- `BEDROCK_MODEL_ID` - Bedrock model to use (default: "anthropic.claude-3-haiku-20240307")
- `BEDROCK_REGION` - AWS region for Bedrock (default: "us-east-1")
- `MAX_TOKENS` - Maximum tokens for AI generation (default: 200)
- `TEMPERATURE` - AI generation temperature (default: 0.7)

## Dependencies

- `boto3==1.34.0` - AWS SDK for Python

## Deployment

1. Install dependencies: `pip install -r requirements.txt -t .`
2. Create deployment package: `zip -r function.zip .`
3. Deploy to AWS Lambda with appropriate IAM role

## IAM Permissions Required

- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`