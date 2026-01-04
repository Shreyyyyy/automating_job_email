"""
Configuration management for the bulk email application.

Loads and validates environment variables for email sending.
Designed to be secure and production-ready.
Supports both local .env files and Streamlit Cloud secrets.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Try to import streamlit for cloud deployment
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


def get_config_value(key: str, default: str = "") -> str:
    """
    Get configuration value from Streamlit secrets or environment variables.
    
    Priority:
    1. Streamlit secrets (for cloud deployment)
    2. Environment variables (for local development)
    3. Default value
    """
    if HAS_STREAMLIT:
        try:
            return st.secrets.get(key, os.getenv(key, default))
        except (AttributeError, FileNotFoundError):
            # Streamlit secrets not available, fall back to env vars
            return os.getenv(key, default)
    return os.getenv(key, default)


class Config:
    """
    Centralized configuration class.
    
    All sensitive data (credentials) are loaded from environment variables
    or Streamlit secrets. This ensures no credentials are hardcoded or 
    exposed to the frontend.
    """
    
    # SMTP Configuration
    SMTP_HOST: str = get_config_value("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(get_config_value("SMTP_PORT", "587"))
    SENDER_EMAIL: str = get_config_value("SENDER_EMAIL", "")
    SENDER_PASSWORD: str = get_config_value("SENDER_PASSWORD", "")
    SENDER_NAME: str = get_config_value("SENDER_NAME", "Job Applicant")
    
    # Email Content
    JOB_TITLE: str = get_config_value("JOB_TITLE", "Software Engineer")
    COMPANY_PREFERENCE: str = get_config_value("COMPANY_PREFERENCE", "your organization")
    
    # Rate Limiting (in seconds)
    MIN_DELAY: int = int(get_config_value("MIN_DELAY", "10"))
    MAX_DELAY: int = int(get_config_value("MAX_DELAY", "15"))
    
    # File Paths
    CV_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cv.pdf")
    COVER_LETTER_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "templates", 
        "cover_letter.txt"
    )
    
    @classmethod
    def validate(cls) -> tuple[bool, Optional[str]]:
        """
        Validate that all required configuration is present.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not cls.SENDER_EMAIL:
            return False, "SENDER_EMAIL not configured in .env file"
        
        if not cls.SENDER_PASSWORD:
            return False, "SENDER_PASSWORD not configured in .env file"
        
        if not os.path.exists(cls.CV_PATH):
            return False, f"CV file not found at {cls.CV_PATH}"
        
        if not os.path.exists(cls.COVER_LETTER_PATH):
            return False, f"Cover letter template not found at {cls.COVER_LETTER_PATH}"
        
        return True, None
    
    @classmethod
    def get_masked_email(cls) -> str:
        """
        Return a masked version of the sender email for display purposes.
        
        Example: j***@gmail.com
        """
        if not cls.SENDER_EMAIL:
            return "Not configured"
        
        parts = cls.SENDER_EMAIL.split("@")
        if len(parts) != 2:
            return "Invalid email"
        
        username, domain = parts
        if len(username) <= 2:
            masked_username = username[0] + "*"
        else:
            masked_username = username[0] + "*" * (len(username) - 2) + username[-1]
        
        return f"{masked_username}@{domain}"


# Export singleton instance
config = Config()
