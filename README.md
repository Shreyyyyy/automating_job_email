# Bulk Job Application Email Sender

A production-ready, mobile-friendly web application for sending bulk job application emails with CV and cover letter attachments.

## Features

- **Smart Email Parsing**: Extract emails from any raw text (WhatsApp messages, social posts, paragraphs)
- **Deduplication**: Automatically removes duplicate email addresses
- **Validation**: Filters out invalid or malformed emails
- **Safe Rate Limiting**: 10-15 second delays between sends to avoid spam blocking
- **Mobile-First UI**: Touch-friendly, clean interface that works on phones
- **Graceful Error Handling**: Continues sending even if individual emails fail
- **Real-time Status**: Shows success/failure count per email

## Tech Stack

- **Frontend**: Streamlit (mobile-optimized)
- **Backend**: Python 3.8+
- **Email**: SMTP (Gmail App Password / SendGrid ready)
- **State**: Session-based (no database)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Email Credentials

Create a `.env` file in the project root:

```env
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SENDER_NAME=Your Name

# Email Content
JOB_TITLE=Software Engineer
COMPANY_PREFERENCE=your preferred companies/roles
```

### 3. Add Your CV

Place your CV as `cv.pdf` in the project root directory.

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage

### Step 1: Paste Text
Paste any text containing email addresses into the large text box. Examples:
- WhatsApp group messages
- Social media posts
- Email lists
- Paragraphs with embedded emails

### Step 2: Parse Emails
Click "Parse Emails" to extract all valid email addresses.

### Step 3: Review
Review the extracted and deduplicated email list.

### Step 4: Send
Click "Send Emails" to start the bulk send process.

### Step 5: Monitor
Watch real-time progress with success/failure counts.

## Gmail App Password Setup

1. Enable 2-Factor Authentication on your Google Account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Use this 16-character password in your `.env` file

## SendGrid Setup (Alternative)

To use SendGrid instead of Gmail:

1. Sign up at [SendGrid](https://sendgrid.com)
2. Generate an API key
3. Update `.env`:
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SENDER_EMAIL=your-verified-sender@example.com
SENDER_PASSWORD=your-sendgrid-api-key
```

## Security Notes

- **Never commit `.env` file** - it's in `.gitignore`
- Credentials are stored server-side only
- No credentials exposed to frontend
- Use environment variables in production

## Mobile Usage Tips

- Works best in landscape mode on phones
- Large touch targets for easy interaction
- Responsive text areas
- Clear visual feedback

## Rate Limiting

- Default: 10-15 second delay between emails
- Prevents spam blocking by email providers
- Configurable in `email_sender.py`

## File Structure

```
email/
├── app.py                 # Main Streamlit application
├── core/
│   ├── email_parser.py    # Email extraction and validation
│   ├── email_sender.py    # SMTP email sending logic
│   └── config.py          # Configuration management
├── templates/
│   └── cover_letter.txt   # Generic cover letter template
├── cv.pdf                 # Your CV (add this)
├── .env                   # Email credentials (create this)
├── .gitignore
├── requirements.txt
└── README.md
```

## Future Enhancements (Not Implemented)

The codebase is designed to support:
- FastAPI backend migration
- React/Next.js frontend
- LLM-based email personalization
- Multiple email provider support
- Usage limits and quotas
- Email history persistence

## Troubleshooting

### Emails not sending
- Check SMTP credentials in `.env`
- Verify Gmail App Password is correct
- Check internet connection
- Review error messages in the UI

### Parsing issues
- Ensure text contains valid email addresses
- Check for unusual formatting
- Try copying text without special characters

### Mobile display issues
- Try landscape orientation
- Refresh the page
- Clear browser cache

## License

MIT License - Free to use and modify

## Support

For issues or questions, please check the troubleshooting section or review the code comments.
