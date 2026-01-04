"""
Test the email formatting to ensure placeholders are replaced correctly.
"""

from core.email_sender import EmailSender
from core.config import config

def test_cover_letter_formatting():
    """Test that cover letter placeholders are properly replaced."""
    
    print("=" * 70)
    print("COVER LETTER FORMATTING TEST")
    print("=" * 70)
    
    # Initialize sender
    sender = EmailSender()
    
    # Get the raw template
    print("\n📄 Raw Template (with placeholders):")
    print("-" * 70)
    print(sender.cover_letter[:300] + "...")
    
    # Format the template
    formatted = sender._format_cover_letter(sender.cover_letter)
    
    print("\n✅ Formatted Cover Letter (placeholders replaced):")
    print("-" * 70)
    print(formatted)
    
    # Verify placeholders are replaced
    print("\n🔍 Verification:")
    print("-" * 70)
    
    has_sender_placeholder = "{sender_name}" in formatted
    has_job_placeholder = "{job_title}" in formatted
    has_company_placeholder = "{company_preference}" in formatted
    
    if has_sender_placeholder:
        print("❌ ERROR: {sender_name} placeholder still present!")
    else:
        print(f"✅ {{sender_name}} placeholder replaced with: {config.SENDER_NAME}")
    
    if has_job_placeholder:
        print("❌ ERROR: {job_title} placeholder still present!")
    else:
        print(f"✅ {{job_title}} placeholder replaced with: {config.JOB_TITLE}")
    
    if has_company_placeholder:
        print("❌ ERROR: {company_preference} placeholder still present!")
    else:
        print(f"✅ {{company_preference}} placeholder replaced with: {config.COMPANY_PREFERENCE}")
    
    print("\n" + "=" * 70)
    
    if not (has_sender_placeholder or has_job_placeholder or has_company_placeholder):
        print("✅ ALL PLACEHOLDERS SUCCESSFULLY REPLACED!")
        print("=" * 70)
        print("\nYour emails will now show the correct sender name and details! 🎉\n")
        return True
    else:
        print("❌ SOME PLACEHOLDERS NOT REPLACED")
        print("=" * 70)
        return False

if __name__ == "__main__":
    test_cover_letter_formatting()
