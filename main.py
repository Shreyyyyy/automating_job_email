"""
FastAPI Bulk Email Sender - Main Application

A production-ready, mobile-friendly API for sending bulk job application emails.
Built with FastAPI for performance and modern async capabilities.

Author: Senior Full-Stack Engineer
Date: 2026-01-04
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import asyncio
from pathlib import Path

from core import config, EmailParser, EmailSender, EmailSendResult

# ============================================================================
# FASTAPI APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Bulk Email Sender API",
    description="Send bulk job application emails with ease",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ParseEmailsRequest(BaseModel):
    text: str

class ParseEmailsResponse(BaseModel):
    valid_emails: List[str]
    invalid_emails: List[str]
    duplicates_info: str
    total_valid: int

class SendEmailsRequest(BaseModel):
    recipient_emails: List[EmailStr]
    speed_mode: str = "safe"  # "instant", "fast", or "safe"

class EmailSendResultModel(BaseModel):
    email: str
    success: bool
    error: Optional[str] = None

class SendEmailsResponse(BaseModel):
    results: List[EmailSendResultModel]
    summary: dict
    elapsed_time: float

class ConfigStatusResponse(BaseModel):
    is_valid: bool
    error_message: Optional[str]
    sender_email: str
    has_default_cv: bool
    smtp_info: str


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main frontend HTML page."""
    html_file = Path(__file__).parent / "static" / "index.html"
    if html_file.exists():
        return html_file.read_text()
    return """
    <html>
        <head><title>Bulk Email Sender</title></head>
        <body>
            <h1>Bulk Email Sender API</h1>
            <p>Frontend not found. Please create static/index.html</p>
            <p><a href="/api/docs">View API Documentation</a></p>
        </body>
    </html>
    """

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "bulk-email-sender"}

@app.get("/api/config/status", response_model=ConfigStatusResponse)
async def get_config_status():
    """Get configuration status."""
    is_valid, error_msg = config.validate()
    
    return ConfigStatusResponse(
        is_valid=is_valid,
        error_message=error_msg,
        sender_email=config.get_masked_email(),
        has_default_cv=config.has_default_cv(),
        smtp_info=f"{config.SMTP_HOST}:{config.SMTP_PORT}"
    )

@app.post("/api/emails/parse", response_model=ParseEmailsResponse)
async def parse_emails(request: ParseEmailsRequest):
    """
    Parse and validate email addresses from text.
    
    Extracts emails from arbitrary text, validates them, and removes duplicates.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    parser = EmailParser()
    valid, invalid, duplicates_info = parser.parse_and_validate(request.text)
    
    return ParseEmailsResponse(
        valid_emails=valid,
        invalid_emails=invalid,
        duplicates_info=duplicates_info[0] if duplicates_info else "0 duplicates removed",
        total_valid=len(valid)
    )

@app.post("/api/emails/send", response_model=SendEmailsResponse)
async def send_emails(
    recipient_emails: str = Form(...),
    speed_mode: str = Form("safe"),
    cv_file: Optional[UploadFile] = File(None)
):
    """
    Send bulk emails to recipients.
    
    Supports three speed modes:
    - instant: Parallel sending (fastest)
    - fast: Sequential without delays
    - safe: Rate-limited (recommended)
    """
    import json
    import time
    
    # Validate configuration
    is_valid, error_msg = config.validate()
    if not is_valid:
        raise HTTPException(status_code=500, detail=f"Configuration error: {error_msg}")
    
    # Parse recipient emails from JSON string
    try:
        emails_list = json.loads(recipient_emails)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid email list format")
    
    if not emails_list:
        raise HTTPException(status_code=400, detail="No recipient emails provided")
    
    # Check if CV is available
    has_cv = cv_file is not None or config.has_default_cv()
    if not has_cv:
        raise HTTPException(status_code=400, detail="No CV available. Please upload a CV file.")
    
    # Read uploaded CV if provided
    uploaded_cv_bytes = None
    uploaded_cv_name = None
    if cv_file:
        uploaded_cv_bytes = await cv_file.read()
        uploaded_cv_name = cv_file.filename
    
    # Initialize sender
    sender = EmailSender()
    
    # Prepare email content
    subject = f"Application for {config.JOB_TITLE} Position"
    body = sender._load_cover_letter()
    body = sender._format_cover_letter(body)
    
    # Track time
    start_time = time.time()
    
    # Send emails based on speed mode
    results = []
    
    if speed_mode == "instant":
        # Concurrent sending
        results = sender.send_bulk_emails_concurrent(
            recipient_emails=emails_list,
            subject=subject,
            body=body,
            max_workers=10,
            uploaded_cv_bytes=uploaded_cv_bytes,
            uploaded_cv_name=uploaded_cv_name
        )
    else:
        # Sequential sending
        min_delay = 0 if speed_mode == "fast" else config.MIN_DELAY
        max_delay = 0 if speed_mode == "fast" else config.MAX_DELAY
        
        results = sender.send_bulk_emails(
            recipient_emails=emails_list,
            subject=subject,
            body=body,
            min_delay=min_delay,
            max_delay=max_delay,
            uploaded_cv_bytes=uploaded_cv_bytes,
            uploaded_cv_name=uploaded_cv_name
        )
    
    elapsed_time = time.time() - start_time
    
    # Convert results to response model
    result_models = [
        EmailSendResultModel(
            email=r.email,
            success=r.success,
            error=r.error
        )
        for r in results
    ]
    
    # Get summary
    summary = sender.get_summary(results)
    
    return SendEmailsResponse(
        results=result_models,
        summary=summary,
        elapsed_time=elapsed_time
    )

@app.get("/api/cover-letter")
async def get_cover_letter():
    """Get the cover letter template preview."""
    try:
        sender = EmailSender()
        template = sender._load_cover_letter()
        formatted = sender._format_cover_letter(template)
        
        return {
            "subject": f"Application for {config.JOB_TITLE} Position",
            "body": formatted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not load cover letter: {str(e)}")


# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print("🚀 Bulk Email Sender API starting up...")
    print(f"📧 Sender: {config.get_masked_email()}")
    print(f"📄 Default CV: {'Available' if config.has_default_cv() else 'Not found'}")
    print(f"🔧 SMTP: {config.SMTP_HOST}:{config.SMTP_PORT}")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print("👋 Bulk Email Sender API shutting down...")


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler."""
    return JSONResponse(
        status_code=500,
        content={"error": f"Internal server error: {str(exc)}"}
    )


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
