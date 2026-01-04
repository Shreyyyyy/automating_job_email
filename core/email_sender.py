"""
Email sending module with SMTP support.

Handles secure email sending with attachments, rate limiting,
and graceful error handling. Production-ready and provider-agnostic.
"""

import smtplib
import time
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Callable, Optional
from pathlib import Path

from .config import config


class EmailSendResult:
    """Result of an email send operation."""
    
    def __init__(self, email: str, success: bool, error: Optional[str] = None):
        self.email = email
        self.success = success
        self.error = error
    
    def __repr__(self):
        status = "✓" if self.success else "✗"
        return f"{status} {self.email}" + (f" - {self.error}" if self.error else "")


class EmailSender:
    """
    Production-ready email sender with SMTP support.
    
    Features:
    - Secure SMTP connection (TLS)
    - PDF attachment support
    - Rate limiting to prevent spam blocking
    - Graceful error handling
    - Progress callbacks
    - Provider-agnostic (Gmail, SendGrid, etc.)
    """
    
    def __init__(
        self,
        smtp_host: str = None,
        smtp_port: int = None,
        sender_email: str = None,
        sender_password: str = None,
        sender_name: str = None
    ):
        """
        Initialize email sender with SMTP credentials.
        
        Args:
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port
            sender_email: Sender email address
            sender_password: Sender password or app password
            sender_name: Display name for sender
        """
        self.smtp_host = smtp_host or config.SMTP_HOST
        self.smtp_port = smtp_port or config.SMTP_PORT
        self.sender_email = sender_email or config.SENDER_EMAIL
        self.sender_password = sender_password or config.SENDER_PASSWORD
        self.sender_name = sender_name or config.SENDER_NAME
        
        # Load email content
        self.cover_letter = self._load_cover_letter()
        self.cv_path = config.CV_PATH
    
    def _load_cover_letter(self) -> str:
        """Load cover letter template from file."""
        try:
            with open(config.COVER_LETTER_PATH, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            # Fallback to a basic template
            return f"""Dear Hiring Manager,

I am writing to express my interest in the {config.JOB_TITLE} position at your organization.

Please find my CV attached for your review. I am excited about the opportunity to contribute to your team.

Thank you for considering my application.

Best regards,
{self.sender_name}"""
    
    def _format_cover_letter(self, template: str) -> str:
        """
        Replace placeholders in cover letter template with actual values.
        
        Args:
            template: Cover letter template with placeholders
            
        Returns:
            Formatted cover letter with values substituted
        """
        # Replace all placeholders with actual config values
        formatted = template.replace("{sender_name}", self.sender_name)
        formatted = formatted.replace("{job_title}", config.JOB_TITLE)
        formatted = formatted.replace("{company_preference}", config.COMPANY_PREFERENCE)
        
        return formatted
    
    def _create_email_message(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        attachment_path: Optional[str] = None,
        attachment_bytes: Optional[bytes] = None,
        attachment_filename: Optional[str] = None
    ) -> MIMEMultipart:
        """
        Create a MIME email message with optional attachment.
        
        Args:
            recipient_email: Recipient's email address
            subject: Email subject line
            body: Email body text
            attachment_path: Path to PDF attachment (for file on disk)
            attachment_bytes: Bytes of PDF attachment (for uploaded file)
            attachment_filename: Name of the attachment file
            
        Returns:
            MIMEMultipart message object
        """
        msg = MIMEMultipart()
        msg['From'] = f"{self.sender_name} <{self.sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Attach body text
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF from bytes (uploaded file)
        if attachment_bytes:
            pdf_attachment = MIMEApplication(attachment_bytes, _subtype='pdf')
            pdf_attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=attachment_filename or 'cv.pdf'
            )
            msg.attach(pdf_attachment)
        # Attach PDF from file path
        elif attachment_path and Path(attachment_path).exists():
            with open(attachment_path, 'rb') as f:
                pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
                pdf_attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=Path(attachment_path).name
                )
                msg.attach(pdf_attachment)
        
        return msg
    
    def send_single_email(
        self,
        recipient_email: str,
        subject: str = None,
        body: str = None,
        attach_cv: bool = True,
        uploaded_cv_bytes: Optional[bytes] = None,
        uploaded_cv_name: Optional[str] = None
    ) -> EmailSendResult:
        """
        Send a single email with optional CV attachment.
        
        Args:
            recipient_email: Recipient's email address
            subject: Email subject (uses default if None)
            body: Email body (uses cover letter if None)
            attach_cv: Whether to attach CV
            uploaded_cv_bytes: Bytes of uploaded CV file (takes precedence over default)
            uploaded_cv_name: Name of uploaded CV file
            
        Returns:
            EmailSendResult object
        """
        # Use defaults if not provided
        if subject is None:
            subject = f"Application for {config.JOB_TITLE} Position"
        
        if body is None:
            # Format the cover letter template with actual values
            body = self._format_cover_letter(self.cover_letter)
        
        try:
            # Create message with uploaded CV or default CV
            if attach_cv and uploaded_cv_bytes:
                msg = self._create_email_message(
                    recipient_email=recipient_email,
                    subject=subject,
                    body=body,
                    attachment_bytes=uploaded_cv_bytes,
                    attachment_filename=uploaded_cv_name
                )
            else:
                msg = self._create_email_message(
                    recipient_email=recipient_email,
                    subject=subject,
                    body=body,
                    attachment_path=self.cv_path if attach_cv else None
                )
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()  # Secure connection
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return EmailSendResult(recipient_email, success=True)
        
        except smtplib.SMTPAuthenticationError:
            return EmailSendResult(
                recipient_email,
                success=False,
                error="Authentication failed - check credentials"
            )
        except smtplib.SMTPException as e:
            return EmailSendResult(
                recipient_email,
                success=False,
                error=f"SMTP error: {str(e)}"
            )
        except Exception as e:
            return EmailSendResult(
                recipient_email,
                success=False,
                error=f"Unexpected error: {str(e)}"
            )
    
    def send_bulk_emails(
        self,
        recipient_emails: List[str],
        subject: str = None,
        body: str = None,
        progress_callback: Optional[Callable[[int, int, EmailSendResult], None]] = None,
        min_delay: int = None,
        max_delay: int = None,
        uploaded_cv_bytes: Optional[bytes] = None,
        uploaded_cv_name: Optional[str] = None
    ) -> List[EmailSendResult]:
        """
        Send emails to multiple recipients with rate limiting.
        
        Args:
            recipient_emails: List of recipient email addresses
            subject: Email subject (uses default if None)
            body: Email body (uses cover letter if None)
            progress_callback: Function called after each email (current, total, result)
            min_delay: Minimum delay between emails in seconds
            max_delay: Maximum delay between emails in seconds
            uploaded_cv_bytes: Bytes of uploaded CV file (takes precedence over default)
            uploaded_cv_name: Name of uploaded CV file
            
        Returns:
            List of EmailSendResult objects
        """
        min_delay = min_delay or config.MIN_DELAY
        max_delay = max_delay or config.MAX_DELAY
        
        results: List[EmailSendResult] = []
        total = len(recipient_emails)
        
        for i, email in enumerate(recipient_emails, 1):
            # Send email
            result = self.send_single_email(
                recipient_email=email,
                subject=subject,
                body=body,
                attach_cv=True,
                uploaded_cv_bytes=uploaded_cv_bytes,
                uploaded_cv_name=uploaded_cv_name
            )
            results.append(result)
            
            # Call progress callback if provided
            if progress_callback:
                progress_callback(i, total, result)
            
            # Rate limiting: wait between sends (except for the last one)
            if i < total:
                delay = random.uniform(min_delay, max_delay)
                time.sleep(delay)
        
        return results
    
    def get_summary(self, results: List[EmailSendResult]) -> dict:
        """
        Generate summary statistics from send results.
        
        Args:
            results: List of EmailSendResult objects
            
        Returns:
            Dictionary with success/failure counts and details
        """
        total = len(results)
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]
        
        return {
            'total': total,
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': (len(successful) / total * 100) if total > 0 else 0,
            'successful_emails': [r.email for r in successful],
            'failed_emails': [(r.email, r.error) for r in failed]
        }


# Example usage
if __name__ == "__main__":
    # This would require proper .env configuration
    sender = EmailSender()
    
    # Test single email
    result = sender.send_single_email("test@example.com")
    print(result)
