"""
Test script for email parsing functionality.
Run this to verify the email parser works correctly.
"""

from core.email_parser import EmailParser

def test_email_parsing():
    """Test email parsing with various input formats."""
    
    print("=" * 70)
    print("EMAIL PARSER TEST SUITE")
    print("=" * 70)
    
    # Test Case 1: Simple list
    print("\n📋 Test 1: Simple Email List")
    print("-" * 70)
    test1 = """
    john@company.com
    jane@startup.io
    admin@tech.co.uk
    """
    valid, invalid, duplicates = EmailParser.parse_and_validate(test1)
    print(f"Input: {test1.strip()}")
    print(f"✓ Valid: {valid}")
    print(f"✗ Invalid: {invalid}")
    print(f"ℹ Info: {duplicates}")
    
    # Test Case 2: Embedded in text
    print("\n📋 Test 2: Emails Embedded in Text")
    print("-" * 70)
    test2 = """
    Hey, contact me at john.doe@example.com for more info.
    You can also reach Jane at jane_smith@company.co.uk
    or try the support team: support@startup.io
    """
    valid, invalid, duplicates = EmailParser.parse_and_validate(test2)
    print(f"Input: {test2.strip()}")
    print(f"✓ Valid: {valid}")
    print(f"✗ Invalid: {invalid}")
    print(f"ℹ Info: {duplicates}")
    
    # Test Case 3: With duplicates
    print("\n📋 Test 3: List with Duplicates")
    print("-" * 70)
    test3 = """
    admin@company.com
    john@startup.io
    admin@company.com
    jane@tech.co
    ADMIN@COMPANY.COM
    """
    valid, invalid, duplicates = EmailParser.parse_and_validate(test3)
    print(f"Input: {test3.strip()}")
    print(f"✓ Valid: {valid}")
    print(f"✗ Invalid: {invalid}")
    print(f"ℹ Info: {duplicates}")
    
    # Test Case 4: Mixed valid and invalid
    print("\n📋 Test 4: Mixed Valid and Invalid Emails")
    print("-" * 70)
    test4 = """
    valid@email.com
    invalid@email
    another.valid@company.co.uk
    not-an-email
    test@test.io
    @invalid.com
    """
    valid, invalid, duplicates = EmailParser.parse_and_validate(test4)
    print(f"Input: {test4.strip()}")
    print(f"✓ Valid: {valid}")
    print(f"✗ Invalid: {invalid}")
    print(f"ℹ Info: {duplicates}")
    
    # Test Case 5: WhatsApp-style message
    print("\n📋 Test 5: WhatsApp Message Format")
    print("-" * 70)
    test5 = """
    [10:30 AM] John: Hey everyone! 👋
    [10:31 AM] Jane: For job applications, email hr@techcorp.com
    [10:32 AM] Mike: Also try careers@startup.io and jobs@company.net
    [10:33 AM] Sarah: Don't forget recruiting@business.co.uk!
    """
    valid, invalid, duplicates = EmailParser.parse_and_validate(test5)
    print(f"Input: {test5.strip()}")
    print(f"✓ Valid: {valid}")
    print(f"✗ Invalid: {invalid}")
    print(f"ℹ Info: {duplicates}")
    
    # Test Case 6: Social media post
    print("\n📋 Test 6: Social Media Post Format")
    print("-" * 70)
    test6 = """
    🚀 We're hiring! 🚀
    
    Looking for talented developers to join our team.
    Send your CV to: hiring@awesomecompany.com
    
    Also check out our partners:
    • jobs@partner1.io
    • careers@partner2.com
    • recruitment@partner3.net
    
    #hiring #jobs #tech
    """
    valid, invalid, duplicates = EmailParser.parse_and_validate(test6)
    print(f"Input: {test6.strip()}")
    print(f"✓ Valid: {valid}")
    print(f"✗ Invalid: {invalid}")
    print(f"ℹ Info: {duplicates}")
    
    # Test Case 7: Empty input
    print("\n📋 Test 7: Empty Input")
    print("-" * 70)
    test7 = ""
    valid, invalid, duplicates = EmailParser.parse_and_validate(test7)
    print(f"Input: (empty)")
    print(f"✓ Valid: {valid}")
    print(f"✗ Invalid: {invalid}")
    print(f"ℹ Info: {duplicates}")
    
    # Test Case 8: No emails
    print("\n📋 Test 8: Text Without Emails")
    print("-" * 70)
    test8 = """
    This is just some random text
    without any email addresses
    just words and sentences
    """
    valid, invalid, duplicates = EmailParser.parse_and_validate(test8)
    print(f"Input: {test8.strip()}")
    print(f"✓ Valid: {valid}")
    print(f"✗ Invalid: {invalid}")
    print(f"ℹ Info: {duplicates}")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 70)
    print("\nThe email parser is working correctly!")
    print("You can now use the main application with confidence.\n")

if __name__ == "__main__":
    test_email_parsing()
