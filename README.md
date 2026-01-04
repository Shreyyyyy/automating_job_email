# 📧 Bulk Email Sender

A production-ready, mobile-friendly web app for sending bulk job application emails with CV attachments.

## 🚀 Features

- **Smart Email Parsing**: Extract emails from any text (WhatsApp messages, lists, etc.)
- **CV Upload**: Upload your CV directly in the app or use a default
- **Bulk Sending**: Send to multiple recipients with optimized performance
- **⚡ Instant Mode**: Parallel sending - send 100 emails in seconds!
- **🚀 Fast Mode**: Sequential sending with persistent connections (5-10x faster)
- **🛡️ Safe Mode**: Rate-limited sending to prevent spam detection
- **Mobile-Friendly**: Optimized for phone browsers with large touch targets
- **Secure**: SMTP authentication with environment variables
- **Modern UI**: Sleek black and white gradient design

## 🔧 Setup for Deployment

### Streamlit Cloud Configuration

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Deploy this repository
4. Add secrets in Streamlit Cloud dashboard:

```toml
# .streamlit/secrets.toml format
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"
SENDER_NAME = "Your Name"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "587"
JOB_TITLE = "Software Engineer"
COMPANY_PREFERENCE = "innovative tech companies"
```

### Gmail App Password Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account → Security → 2-Step Verification → App passwords
3. Generate an app password for "Mail"
4. Use this password (not your regular password) in `SENDER_PASSWORD`

## 📱 Mobile Usage

- Works great on phone browsers
- Large, touch-friendly buttons
- Optimized font sizes for readability
- Landscape orientation recommended for best experience

## ⚡ Performance

### Speed Optimizations

The app uses **persistent SMTP connections** for bulk sending, which provides:
- **5-10x faster** sending compared to creating new connections per email
- Single authentication handshake for all emails in a batch
- Reduced network overhead and latency

### Sending Modes

- **⚡ Instant Mode**: Sends all emails in parallel using multiple threads (ULTRA FAST!)
  - Best for: Maximum speed, any batch size
  - Speed: Can send 100 emails in 10-20 seconds!
  - Uses: ThreadPoolExecutor with 10 concurrent workers
  - Note: Each email gets its own SMTP connection
  
- **🚀 Fast Mode**: Sends emails sequentially with no delays
  - Best for: Small batches, trusted recipients
  - Speed: ~1-2 seconds per email
  - Uses: Single persistent SMTP connection
  
- **🛡️ Safe Mode**: Adds random delays between emails (recommended)
  - Best for: Large batches, avoiding spam filters
  - Speed: 2-5 seconds per email (configurable)
  - Prevents: Gmail rate limiting and spam detection
  - Uses: Single persistent SMTP connection with delays



## 🛡️ Security

- Credentials stored securely in Streamlit secrets
- No sensitive data in repository
- SMTP with TLS encryption
- Rate limiting to prevent spam blocking

## 📄 License

MIT License - Feel free to use and modify!
