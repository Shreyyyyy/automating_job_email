"""
Configuration management for the bulk email application.

Loads and validates environment variables for email sending.
Designed to be secure and production-ready.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Centralized configuration class.
    
    All sensitive data (credentials) are loaded from environment variables.
    This ensures no credentials are hardcoded or exposed to the frontend.
    """
    
    # SMTP Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "")
    SENDER_PASSWORD: str = os.getenv("SENDER_PASSWORD", "")
    SENDER_NAME: str = os.getenv("SENDER_NAME", "Job Applicant")
    
    # Email Content
    JOB_TITLE: str = os.getenv("JOB_TITLE", "Software Engineer")
    COMPANY_PREFERENCE: str = os.getenv("COMPANY_PREFERENCE", "your organization")
    
    # Rate Limiting (in seconds)
    MIN_DELAY: int = int(os.getenv("MIN_DELAY", "10"))
    MAX_DELAY: int = int(os.getenv("MAX_DELAY", "15"))
    
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
