"""
Environment configuration handler for CloudHoroscopeFunction
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration class with environment variable defaults"""
    
    # Project and author information (Requirements 4.4, 4.5)
    project_name: str = "Cloud Horoscope"
    author_name: str = "Unknown Author"
    
    # Default welcome message (Requirement 7.5)
    default_message: str = "Welcome to Cloud Horoscope powered by AWS!"
    
    # Bedrock configuration (Requirement 7.4)
    bedrock_model_id: str = "anthropic.claude-3-haiku-20240307"
    bedrock_region: str = "us-east-1"
    
    # Response configuration
    max_tokens: int = 200
    temperature: float = 0.7
    
    @classmethod
    def from_environment(cls) -> 'Config':
        """
        Create configuration from environment variables with fallback to defaults
        
        Returns:
            Config instance with values from environment or defaults
            
        Raises:
            ValueError: If environment variables contain invalid values
        """
        # Get values from environment with defaults
        project_name = os.getenv('PROJECT_NAME', cls.project_name)
        author_name = os.getenv('AUTHOR_NAME', cls.author_name)
        default_message = os.getenv('DEFAULT_MESSAGE', cls.default_message)
        bedrock_model_id = os.getenv('BEDROCK_MODEL_ID', cls.bedrock_model_id)
        bedrock_region = os.getenv('BEDROCK_REGION', cls.bedrock_region)
        
        # Validate string lengths
        if len(project_name) > 100:
            raise ValueError("PROJECT_NAME must be 100 characters or less")
        if len(author_name) > 100:
            raise ValueError("AUTHOR_NAME must be 100 characters or less")
        if len(default_message) > 500:
            raise ValueError("DEFAULT_MESSAGE must be 500 characters or less")
            
        # Validate Bedrock region (warn if not in common regions)
        common_bedrock_regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']
        if bedrock_region not in common_bedrock_regions:
            print(f"Warning: {bedrock_region} may not support Bedrock service")
        
        # Parse numeric values with validation
        try:
            max_tokens = int(os.getenv('MAX_TOKENS', str(cls.max_tokens)))
            if max_tokens < 50 or max_tokens > 1000:
                raise ValueError("MAX_TOKENS must be between 50 and 1000")
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("MAX_TOKENS must be a valid integer")
            raise
            
        try:
            temperature = float(os.getenv('TEMPERATURE', str(cls.temperature)))
            if temperature < 0.0 or temperature > 1.0:
                raise ValueError("TEMPERATURE must be between 0.0 and 1.0")
        except ValueError as e:
            if "could not convert" in str(e):
                raise ValueError("TEMPERATURE must be a valid float")
            raise
        
        return cls(
            project_name=project_name,
            author_name=author_name,
            default_message=default_message,
            bedrock_model_id=bedrock_model_id,
            bedrock_region=bedrock_region,
            max_tokens=max_tokens,
            temperature=temperature
        )
    
    def get_project_name(self) -> str:
        """Get project name for response formatting"""
        return self.project_name
    
    def get_author_name(self) -> str:
        """Get author name for response formatting"""
        return self.author_name
    
    def get_bedrock_config(self) -> dict:
        """Get Bedrock configuration dictionary"""
        return {
            'model_id': self.bedrock_model_id,
            'region': self.bedrock_region,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature
        }


# Global configuration instance
config = Config.from_environment()