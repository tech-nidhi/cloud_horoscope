# Environment Variables Configuration

## Required Environment Variables
None - all environment variables have default values for basic functionality.

## Optional Environment Variables

### Application Configuration
| Variable | Default Value | Description | Example |
|----------|---------------|-------------|---------|
| `PROJECT_NAME` | "Cloud Horoscope" | Name of the project returned in responses | "My Horoscope App" |
| `AUTHOR_NAME` | "Unknown Author" | Author name returned in responses | "John Doe" |
| `DEFAULT_MESSAGE` | "Welcome to Cloud Horoscope powered by AWS!" | Default message when no horoscope is generated | "Custom welcome message" |

### AWS Bedrock Configuration
| Variable | Default Value | Description | Example |
|----------|---------------|-------------|---------|
| `BEDROCK_MODEL_ID` | "anthropic.claude-3-haiku-20240307" | Bedrock model ID for horoscope generation | "anthropic.claude-3-sonnet-20240229" |
| `BEDROCK_REGION` | "us-east-1" | AWS region for Bedrock service | "us-west-2" |

## Environment Variable Validation

The application validates environment variables on startup:

```python
# In config.py
def get_config():
    config = Config()
    
    # Validate PROJECT_NAME
    if len(config.project_name) > 100:
        raise ValueError("PROJECT_NAME must be 100 characters or less")
    
    # Validate AUTHOR_NAME  
    if len(config.author_name) > 100:
        raise ValueError("AUTHOR_NAME must be 100 characters or less")
    
    # Validate BEDROCK_REGION
    valid_regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']
    if config.bedrock_region not in valid_regions:
        print(f"Warning: {config.bedrock_region} may not support Bedrock")
    
    return config
```

## AWS Lambda Configuration

### Setting Environment Variables in AWS Console
1. Open AWS Lambda console
2. Select your function
3. Go to Configuration → Environment variables
4. Add key-value pairs as needed

### Setting Environment Variables via AWS CLI
```bash
aws lambda update-function-configuration \
    --function-name cloud-horoscope-function \
    --environment Variables='{
        "PROJECT_NAME":"My Horoscope App",
        "AUTHOR_NAME":"John Doe",
        "BEDROCK_REGION":"us-west-2"
    }'
```

### Setting Environment Variables via CloudFormation
```yaml
Resources:
  CloudHoroscopeFunction:
    Type: AWS::Lambda::Function
    Properties:
      Environment:
        Variables:
          PROJECT_NAME: "My Horoscope App"
          AUTHOR_NAME: "John Doe"
          BEDROCK_REGION: "us-west-2"
```

## Security Considerations

- **No Secrets**: This application doesn't require secret environment variables
- **IAM Permissions**: Access to Bedrock is controlled via IAM roles, not environment variables
- **Input Validation**: All environment variables are validated and have safe defaults
- **Logging**: Environment variable values are not logged to prevent information disclosure

## Testing Environment Variables

For local testing, create a `.env` file (not included in deployment):

```bash
# .env file for local testing
PROJECT_NAME="Test Horoscope App"
AUTHOR_NAME="Test Author"
BEDROCK_REGION="us-east-1"
```

Load with python-dotenv in test environment:
```python
from dotenv import load_dotenv
load_dotenv()  # Only for local testing
```