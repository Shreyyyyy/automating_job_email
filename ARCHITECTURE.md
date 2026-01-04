# Architecture & Design Documentation

## Overview

This is a production-ready bulk email sender designed with **simplicity**, **security**, and **future extensibility** in mind.

## Design Principles

### 1. **Separation of Concerns**
- **Core Logic** (`core/`): Pure Python, framework-agnostic
- **UI Layer** (`app.py`): Streamlit-specific presentation
- **Configuration** (`config.py`): Centralized settings management

This separation makes it trivial to swap Streamlit for FastAPI + React later.

### 2. **Security First**
- No credentials in code
- Environment variables for all secrets
- Server-side only credential access
- Masked email display
- `.gitignore` protection

### 3. **Mobile-First Design**
- Touch-friendly buttons (3.5rem height)
- Responsive layout
- Large text areas
- Gradient aesthetics for premium feel
- Works in landscape/portrait

### 4. **Graceful Degradation**
- Continues sending even if individual emails fail
- Clear error messages per recipient
- No cascading failures

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│                      (Streamlit - app.py)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Paste Text   │→ │ Parse Emails │→ │ Send Emails  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       CORE LOGIC LAYER                       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  EmailParser                                          │  │
│  │  • Regex extraction                                   │  │
│  │  • Email validation (email-validator)                 │  │
│  │  • Deduplication (case-insensitive)                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  EmailSender                                          │  │
│  │  • SMTP/TLS connection                                │  │
│  │  • PDF attachment handling                            │  │
│  │  • Rate limiting (10-15s delays)                      │  │
│  │  • Progress callbacks                                 │  │
│  │  • Error handling per email                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Config                                               │  │
│  │  • Environment variable loading                       │  │
│  │  • Validation                                         │  │
│  │  • Secure credential management                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                         │
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │ Gmail SMTP   │   or    │ SendGrid     │                 │
│  │ smtp.gmail   │         │ smtp.sendgrid│                 │
│  └──────────────┘         └──────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

```
email/
├── app.py                      # Main Streamlit UI
├── core/
│   ├── __init__.py            # Package exports
│   ├── config.py              # Configuration management
│   ├── email_parser.py        # Email extraction & validation
│   └── email_sender.py        # SMTP sending logic
├── templates/
│   └── cover_letter.txt       # Email body template
├── cv.pdf                     # User's CV (or generated sample)
├── .env                       # Credentials (gitignored)
├── .env.example               # Template for .env
├── requirements.txt           # Python dependencies
├── README.md                  # User documentation
├── ARCHITECTURE.md            # This file
├── QUICKSTART.py              # Interactive setup guide
├── test_parser.py             # Email parser tests
└── generate_sample_cv.py      # Sample CV generator
```

## Data Flow

### Email Parsing Flow
```
Raw Text Input
    ↓
Regex Extraction (EMAIL_PATTERN)
    ↓
Deduplication (case-insensitive set)
    ↓
Validation (email-validator library)
    ↓
[Valid Emails] + [Invalid Emails] + [Duplicate Count]
```

### Email Sending Flow
```
List of Valid Emails
    ↓
For each email:
    ↓
    Create MIME Message
        ↓
        Add Headers (From, To, Subject)
        ↓
        Attach Body (cover letter)
        ↓
        Attach PDF (CV)
    ↓
    Connect to SMTP (TLS)
    ↓
    Authenticate
    ↓
    Send Message
    ↓
    Record Result (success/failure)
    ↓
    Rate Limit Delay (10-15s)
    ↓
Next Email
```

## Key Design Decisions

### Why Streamlit?
- **Rapid Development**: Build UI in pure Python
- **Mobile Compatible**: Responsive out of the box
- **Session State**: Built-in state management
- **Easy Deployment**: One command to run

**Migration Path**: Core logic is framework-agnostic. To migrate:
1. Keep `core/` as-is
2. Build FastAPI endpoints wrapping core functions
3. Build React frontend calling API
4. Zero changes to business logic

### Why SMTP (not API)?
- **Universal**: Works with any email provider
- **Free**: No API costs
- **Simple**: Standard protocol
- **Flexible**: Easy to switch providers

**Future Enhancement**: Add SendGrid/Mailgun API support alongside SMTP.

### Why No Database?
- **Simplicity**: No setup required
- **Privacy**: No data persistence
- **Stateless**: Session-based only
- **Free**: No hosting costs

**Migration Path**: Add database layer when needed:
```python
# Future: database/models.py
class EmailCampaign(Model):
    emails = JSONField()
    results = JSONField()
    created_at = DateTimeField()
```

### Why Rate Limiting?
- **Spam Prevention**: Avoid being flagged
- **Provider Limits**: Respect SMTP quotas
- **Deliverability**: Better inbox placement

**Current**: Random 10-15s delays
**Future**: Adaptive rate limiting based on provider response

## Security Considerations

### Current Implementation
✅ Environment variables for credentials  
✅ No credentials in code  
✅ `.gitignore` for `.env`  
✅ Server-side only credential access  
✅ TLS for SMTP connections  
✅ Masked email display  

### Future Enhancements
- [ ] OAuth2 for Gmail (instead of app passwords)
- [ ] Encrypted credential storage
- [ ] User authentication
- [ ] Rate limiting per user
- [ ] Audit logging

## Performance

### Current Metrics
- **Parsing**: ~instant for <1000 emails
- **Sending**: 10-15s per email (rate limited)
- **Memory**: Minimal (no large data structures)

### Scalability
- **Current**: Suitable for 1-100 emails per session
- **Bottleneck**: SMTP rate limits (not code)
- **Future**: Queue-based async sending for 1000+ emails

## Testing Strategy

### Current Tests
- ✅ Email parser unit tests (`test_parser.py`)
- ✅ 8 test cases covering edge cases
- ✅ Manual UI testing

### Future Tests
- [ ] Email sender unit tests (mocked SMTP)
- [ ] Integration tests (test SMTP server)
- [ ] E2E tests (Selenium/Playwright)
- [ ] Load tests (concurrent sends)

## Deployment Options

### Option 1: Local (Current)
```bash
streamlit run app.py
```
**Use Case**: Personal use, testing

### Option 2: Local Network (Mobile Access)
```bash
streamlit run app.py --server.address 0.0.0.0
# Access from phone: http://YOUR_IP:8501
```
**Use Case**: Use from phone on same WiFi

### Option 3: Cloud (Streamlit Cloud)
```bash
# Push to GitHub
# Connect Streamlit Cloud
# Add secrets in dashboard
```
**Use Case**: Public/shared access

### Option 4: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```
**Use Case**: Containerized deployment

### Option 5: Production (Future)
```
FastAPI Backend (Docker)
    ↓
React Frontend (Vercel/Netlify)
    ↓
PostgreSQL (Supabase/Railway)
```

## Future Roadmap

### Phase 1: Current ✅
- [x] Email parsing
- [x] SMTP sending
- [x] Rate limiting
- [x] Mobile UI
- [x] Error handling

### Phase 2: Enhanced Features
- [ ] LLM-based email personalization
- [ ] Multiple email templates
- [ ] Scheduling (send later)
- [ ] Email preview before send
- [ ] Attachment customization per recipient

### Phase 3: Multi-User
- [ ] User authentication
- [ ] Campaign history
- [ ] Analytics dashboard
- [ ] Team collaboration
- [ ] Usage quotas

### Phase 4: Enterprise
- [ ] API access
- [ ] Webhooks
- [ ] Custom SMTP servers
- [ ] White-label deployment
- [ ] SLA guarantees

## Code Quality

### Current Standards
- ✅ Type hints where beneficial
- ✅ Docstrings for all functions
- ✅ Clear variable names
- ✅ Separation of concerns
- ✅ Error handling
- ✅ Comments for complex logic

### Future Improvements
- [ ] Full type coverage (mypy)
- [ ] Linting (ruff/pylint)
- [ ] Code formatting (black)
- [ ] Pre-commit hooks
- [ ] CI/CD pipeline

## Monitoring & Observability

### Current
- Console output
- Streamlit UI feedback
- Error messages

### Future
- [ ] Structured logging
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring
- [ ] Email delivery tracking
- [ ] Analytics (Mixpanel/PostHog)

## Conclusion

This application is built as a **simple, working product** with a **clear path to scale**.

Every design decision prioritizes:
1. **User experience** (mobile-first, clear UI)
2. **Security** (no exposed credentials)
3. **Maintainability** (clean code, separation of concerns)
4. **Extensibility** (easy to add features)

The architecture supports evolution from a personal tool to an enterprise SaaS without rewriting core logic.
