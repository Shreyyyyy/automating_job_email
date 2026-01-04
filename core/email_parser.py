"""
Email parsing and validation module.

Extracts email addresses from arbitrary text, validates them,
and removes duplicates. Designed to handle messy real-world input.
"""

import re
from typing import List, Set
from email_validator import validate_email, EmailNotValidError


class EmailParser:
    """
    Robust email parser for extracting emails from unstructured text.
    
    Handles:
    - Emails embedded in paragraphs
    - WhatsApp messages
    - Social media posts
    - Lists with various separators
    """
    
    # Comprehensive regex pattern for email extraction
    # Matches most valid email formats while avoiding false positives
    EMAIL_PATTERN = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """
        Extract all potential email addresses from text.
        
        Args:
            text: Raw text that may contain email addresses
            
        Returns:
            List of potential email addresses (may include invalid ones)
        """
        if not text or not text.strip():
            return []
        
        # Find all matches using regex
        potential_emails = EmailParser.EMAIL_PATTERN.findall(text)
        
        return potential_emails
    
    @staticmethod
    def validate_email_address(email: str) -> bool:
        """
        Validate a single email address using email-validator library.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Normalize and validate
            validation = validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False
    
    @staticmethod
    def deduplicate_emails(emails: List[str]) -> List[str]:
        """
        Remove duplicate emails (case-insensitive).
        
        Args:
            emails: List of email addresses
            
        Returns:
            Deduplicated list of emails
        """
        # Use a set for deduplication (lowercase for case-insensitive comparison)
        seen: Set[str] = set()
        unique_emails: List[str] = []
        
        for email in emails:
            email_lower = email.lower()
            if email_lower not in seen:
                seen.add(email_lower)
                unique_emails.append(email)  # Keep original case
        
        return unique_emails
    
    @staticmethod
    def parse_and_validate(text: str) -> tuple[List[str], List[str], List[str]]:
        """
        Complete parsing pipeline: extract, validate, and deduplicate.
        
        Args:
            text: Raw text containing email addresses
            
        Returns:
            tuple: (valid_emails, invalid_emails, duplicates_removed)
        """
        # Step 1: Extract all potential emails
        potential_emails = EmailParser.extract_emails(text)
        
        if not potential_emails:
            return [], [], []
        
        # Step 2: Deduplicate
        unique_emails = EmailParser.deduplicate_emails(potential_emails)
        duplicates_count = len(potential_emails) - len(unique_emails)
        
        # Step 3: Validate each email
        valid_emails: List[str] = []
        invalid_emails: List[str] = []
        
        for email in unique_emails:
            if EmailParser.validate_email_address(email):
                valid_emails.append(email)
            else:
                invalid_emails.append(email)
        
        return valid_emails, invalid_emails, [f"{duplicates_count} duplicates removed"]
    
    @staticmethod
    def format_email_list(emails: List[str], max_display: int = 50) -> str:
        """
        Format email list for display.
        
        Args:
            emails: List of email addresses
            max_display: Maximum number of emails to display
            
        Returns:
            Formatted string representation
        """
        if not emails:
            return "No emails found"
        
        if len(emails) <= max_display:
            return "\n".join(f"{i+1}. {email}" for i, email in enumerate(emails))
        else:
            displayed = "\n".join(f"{i+1}. {email}" for i, email in enumerate(emails[:max_display]))
            remaining = len(emails) - max_display
            return f"{displayed}\n\n... and {remaining} more"


# Example usage and testing
if __name__ == "__main__":
    # Test with sample text
    sample_text = """
    Hey, here are some contacts:
    john.doe@example.com
    Contact Jane at jane_smith@company.co.uk
    
    Also try:
    - admin@startup.io
    - support@tech-company.com
    - invalid@email (this should be filtered)
    - john.doe@example.com (duplicate)
    
    WhatsApp message: "Email me at mobile.user@gmail.com"
    """
    
    parser = EmailParser()
    valid, invalid, duplicates = parser.parse_and_validate(sample_text)
    
    print("Valid emails:", valid)
    print("Invalid emails:", invalid)
    print("Duplicates info:", duplicates)
