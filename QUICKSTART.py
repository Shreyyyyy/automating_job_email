"""
Quick Start Guide for Bulk Email Sender
========================================

This guide will help you set up and run the application in under 5 minutes.
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║          📧 BULK EMAIL SENDER - QUICK START GUIDE 📧          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

STEP 1: Install Dependencies
─────────────────────────────
Run: pip install -r requirements.txt

STEP 2: Configure Email Settings
─────────────────────────────────
1. Open the .env file
2. Update these fields:
   
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   SENDER_NAME=Your Full Name
   JOB_TITLE=Software Engineer

3. For Gmail App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Enable 2FA first
   - Generate app password for "Mail"
   - Use the 16-character password

STEP 3: Prepare Your CV
────────────────────────
- Place your CV as 'cv.pdf' in the project root
- Or use the sample CV we generated for you

STEP 4: Run the Application
────────────────────────────
Run: streamlit run app.py

The app will open at: http://localhost:8501

STEP 5: Use the App
───────────────────
1. Paste text containing email addresses
2. Click "Parse Emails"
3. Review extracted emails
4. Click "Send Emails"
5. Monitor progress

╔════════════════════════════════════════════════════════════════╗
║                        MOBILE USAGE                            ║
╚════════════════════════════════════════════════════════════════╝

To use on your phone:
1. Find your computer's local IP: ifconfig or ipconfig
2. Run: streamlit run app.py --server.address 0.0.0.0
3. On phone, visit: http://YOUR_IP:8501
4. Use landscape mode for best experience

╔════════════════════════════════════════════════════════════════╗
║                      SECURITY NOTES                            ║
╚════════════════════════════════════════════════════════════════╝

✓ Never commit .env file to git (it's already in .gitignore)
✓ Use app passwords, not your main password
✓ Credentials stay server-side only
✓ No data is stored or logged

╔════════════════════════════════════════════════════════════════╗
║                    TROUBLESHOOTING                             ║
╚════════════════════════════════════════════════════════════════╝

Problem: "Configuration Error"
Solution: Check .env file has correct values

Problem: "Authentication failed"
Solution: Verify Gmail app password is correct

Problem: Emails not sending
Solution: 
  - Check internet connection
  - Verify SMTP settings
  - Try with fewer emails first

Problem: No emails parsed
Solution: Ensure text contains valid email addresses

╔════════════════════════════════════════════════════════════════╗
║                      SAMPLE TEXT                               ║
╚════════════════════════════════════════════════════════════════╝

Try pasting this sample text:

    Contact us at:
    - hiring@techcorp.com
    - jobs@startup.io
    - hr@company.co.uk
    
    Or email john.doe@example.com directly
    Also try jane_smith@business.net

╔════════════════════════════════════════════════════════════════╗
║                     RATE LIMITING                              ║
╚════════════════════════════════════════════════════════════════╝

Default: 10-15 seconds between emails
This prevents spam blocking by email providers

For 10 emails: ~2-3 minutes total
For 50 emails: ~10-12 minutes total

╔════════════════════════════════════════════════════════════════╗
║                    READY TO START!                             ║
╚════════════════════════════════════════════════════════════════╝

Run this command to start:

    streamlit run app.py

Good luck with your job applications! 🚀
""")
