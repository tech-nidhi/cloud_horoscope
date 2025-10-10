# Lambda Deployment Package Structure

## Directory Structure
```
lambda_function/
├── lambda_function.py          # Main Lambda handler
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── iam-policy.json            # IAM policy document
├── deployment-structure.md     # This file
├── environment-variables.md    # Environment variable documentation
└── tests/                     # Test files (not included in deployment)
    ├── test_zodiac_calculation.py
    ├── test_input_validation.py
    ├── test_bedrock_integration.py
    ├── test_response_formatting.py
    └── test_integration_handler.py
```

## Deployment Package Contents
The following files should be included in the Lambda deployment package:

### Required Files
- `lambda_function.py` - Main entry point
- `config.py` - Configuration handler
- `requirements.txt` - Dependencies

### Optional Files
- `iam-policy.json` - For reference during deployment
- `environment-variables.md` - Documentation for deployment

### Excluded Files
- All test files (`test_*.py`)
- `README.md` - Development documentation
- `deployment-structure.md` - This documentation file

## Deployment Steps
1. Install dependencies: `pip install -r requirements.txt -t .`
2. Create ZIP package with lambda_function.py, config.py, and installed dependencies
3. Upload to AWS Lambda
4. Configure environment variables as documented in environment-variables.md
5. Attach IAM role with permissions from iam-policy.json

## Package Size Considerations
- Current package size should be minimal (< 1MB)
- boto3 is available in Lambda runtime, but included for version consistency
- No additional binary dependencies required