"""
Bulk Job Application Email Sender - Main Application

A production-ready, mobile-friendly web app for sending bulk job application emails.
Built with Streamlit for simplicity and ease of use.

Author: Senior Full-Stack Engineer
Date: 2026-01-04
"""

import streamlit as st
import time
from typing import List
from pathlib import Path

from core import config, EmailParser, EmailSender, EmailSendResult


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Bulk Email Sender",
    page_icon="📧",
    layout="centered",  # Better for mobile
    initial_sidebar_state="collapsed"  # Clean mobile experience
)


# ============================================================================
# CUSTOM CSS FOR MOBILE-FIRST DESIGN
# ============================================================================

st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Mobile-first responsive design with dark background */
    .main {
        padding: 1rem;
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    
    /* Large, touch-friendly buttons */
    .stButton > button {
        width: 100%;
        height: 4rem;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 1rem;
        margin: 0.75rem 0;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(255, 255, 255, 0.15);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Primary action button - Black to Gray gradient */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #000000 0%, #434343 100%);
        color: white;
        border: 2px solid #ffffff;
        box-shadow: 0 4px 16px rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1a1a1a 0%, #5a5a5a 100%);
        box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
    }
    
    /* Secondary action button - White to Gray gradient */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #ffffff 0%, #d0d0d0 100%);
        color: #000000;
        border: 2px solid #000000;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #f5f5f5 0%, #b0b0b0 100%);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        font-size: 1.1rem;
        border-radius: 1rem;
        border: 2px solid #404040;
        padding: 1.25rem;
        min-height: 250px;
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        color: #ffffff;
        line-height: 1.6;
    }
    
    .stTextArea textarea:focus {
        border-color: #ffffff;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2);
        background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
    }
    
    .stTextArea textarea::placeholder {
        color: #808080;
    }
    
    /* Success/Error messages */
    .success-box {
        background: linear-gradient(135deg, #2a2a2a 0%, #404040 100%);
        color: white;
        padding: 1.75rem;
        border-radius: 1rem;
        margin: 1rem 0;
        font-weight: 500;
        font-size: 1.1rem;
        box-shadow: 0 4px 16px rgba(255, 255, 255, 0.15);
        border: 2px solid #ffffff;
    }
    
    .error-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        color: white;
        padding: 1.75rem;
        border-radius: 1rem;
        margin: 1rem 0;
        font-weight: 500;
        font-size: 1.1rem;
        box-shadow: 0 4px 16px rgba(255, 255, 255, 0.15);
        border: 2px solid #808080;
    }
    
    .info-box {
        background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
        color: #1a1a1a;
        padding: 1.75rem;
        border-radius: 1rem;
        margin: 1rem 0;
        font-weight: 500;
        font-size: 1.1rem;
        border: 2px solid #000000;
    }
    
    /* Email list styling */
    .email-list {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        padding: 1.25rem;
        border-radius: 1rem;
        max-height: 350px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 1rem;
        margin: 1rem 0;
        border: 2px solid #404040;
        color: #ffffff;
        line-height: 1.8;
    }
    
    /* Progress bar customization */
    .stProgress > div > div {
        background: linear-gradient(90deg, #000000 0%, #ffffff 50%, #000000 100%);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    /* Header styling */
    h1 {
        color: #ffffff;
        font-weight: 800;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
        text-shadow: 0 2px 8px rgba(255, 255, 255, 0.4);
        letter-spacing: -0.02em;
    }
    
    h2, h3 {
        color: #ffffff;
        font-weight: 700;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 16px rgba(255, 255, 255, 0.1);
        margin: 0.75rem 0;
        text-align: center;
        border: 2px solid #404040;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(255, 255, 255, 0.2);
        border-color: #ffffff;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a0a0a0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #b0b0b0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.75rem;
        font-weight: 600;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border-radius: 1rem;
        border: 2px solid #404040;
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 1rem;
    }
    
    /* Info/warning/success boxes from Streamlit */
    .stAlert {
        border-radius: 1rem;
        border: 2px solid #404040;
        font-size: 1.05rem;
        padding: 1.25rem;
    }
    
    /* Divider */
    hr {
        border-color: #404040;
        margin: 2rem 0;
    }
    
    /* File uploader styling */
    .stFileUploader {
        border-radius: 1rem;
        border: 2px dashed #404040;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #ffffff;
        background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
    }
    
    .stFileUploader label {
        color: #ffffff !important;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .stFileUploader > div {
        color: #b0b0b0;
    }
    
    .stFileUploader button {
        background: linear-gradient(135deg, #ffffff 0%, #d0d0d0 100%) !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .main {
            padding: 0.75rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .stButton > button {
            height: 3.5rem;
            font-size: 1.1rem;
            border-radius: 0.75rem;
        }
        
        .metric-value {
            font-size: 2.25rem;
        }
        
        .metric-card {
            padding: 1.5rem;
        }
        
        .stTextArea textarea {
            font-size: 1rem;
            min-height: 200px;
        }
    }
    
    /* Extra small phones */
    @media (max-width: 480px) {
        h1 {
            font-size: 1.75rem;
        }
        
        .stButton > button {
            height: 3.25rem;
            font-size: 1rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'parsed_emails' not in st.session_state:
    st.session_state.parsed_emails = []

if 'send_results' not in st.session_state:
    st.session_state.send_results = []

if 'is_sending' not in st.session_state:
    st.session_state.is_sending = False

if 'uploaded_cv' not in st.session_state:
    st.session_state.uploaded_cv = None



# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_configuration() -> tuple[bool, str]:
    """Validate app configuration before allowing email operations."""
    is_valid, error_msg = config.validate()
    return is_valid, error_msg or ""


def display_email_list(emails: List[str], title: str = "Extracted Emails"):
    """Display formatted email list."""
    if not emails:
        return
    
    st.markdown(f"**{title}** ({len(emails)} total)")
    email_text = "\n".join(f"{i+1}. {email}" for i, email in enumerate(emails))
    st.markdown(f'<div class="email-list">{email_text}</div>', unsafe_allow_html=True)


def display_metrics(results: List[EmailSendResult]):
    """Display send results as metrics."""
    if not results:
        return
    
    summary = EmailSender().get_summary(results)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary['total']}</div>
            <div class="metric-label">Total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #10b981;">{summary['successful']}</div>
            <div class="metric-label">Sent ✓</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #ef4444;">{summary['failed']}</div>
            <div class="metric-label">Failed ✗</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application logic."""
    
    # Header
    st.title("📧 Bulk Email Sender")
    st.markdown("**Send job applications to multiple companies effortlessly**")
    
    # Configuration validation
    is_valid, error_msg = validate_configuration()
    
    if not is_valid:
        st.markdown(f'<div class="error-box">⚠️ Configuration Error: {error_msg}</div>', 
                   unsafe_allow_html=True)
        st.info("""
        **Setup Instructions:**
        1. Create a `.env` file (copy from `.env.example`)
        2. Add your email credentials
        3. Place your CV as `cv.pdf` in the project root
        4. Restart the application
        """)
        return
    
    # Show configuration status
    with st.expander("📋 Configuration Status", expanded=False):
        st.success(f"✓ Sender: {config.get_masked_email()}")
        st.success(f"✓ CV: {Path(config.CV_PATH).name}")
        st.success(f"✓ SMTP: {config.SMTP_HOST}:{config.SMTP_PORT}")
        st.info(f"Rate Limit: {config.MIN_DELAY}-{config.MAX_DELAY}s between emails")
    
    # ========================================================================
    # CV UPLOAD SECTION
    # ========================================================================
    
    st.markdown("### 📄 Upload Your CV")
    st.markdown("Upload a PDF file to use as your CV attachment (optional - will use default if not uploaded)")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload your CV in PDF format",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_cv = uploaded_file
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.markdown(f"""
        <div class="success-box">
            ✓ CV Uploaded: <strong>{uploaded_file.name}</strong> ({file_size_mb:.2f} MB)
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.uploaded_cv is not None:
        file_size_mb = len(st.session_state.uploaded_cv.getvalue()) / (1024 * 1024)
        st.markdown(f"""
        <div class="info-box" style="background: linear-gradient(135deg, #2a2a2a 0%, #404040 100%); color: white;">
            📎 Using: <strong>{st.session_state.uploaded_cv.name}</strong> ({file_size_mb:.2f} MB)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="info-box">
            📎 Using default CV: <strong>{Path(config.CV_PATH).name}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    
    # ========================================================================
    # STEP 1: PASTE TEXT
    # ========================================================================
    
    st.markdown("### 📝 Step 1: Paste Text with Emails")
    st.markdown("Paste any text containing email addresses (WhatsApp messages, lists, paragraphs, etc.)")
    
    input_text = st.text_area(
        label="Input Text",
        placeholder="Paste your text here...\n\nExample:\nContact john@company.com or jane@startup.io\nAlso try admin@tech.co",
        height=200,
        label_visibility="collapsed"
    )
    
    # ========================================================================
    # STEP 2: PARSE EMAILS
    # ========================================================================
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        parse_button = st.button("🔍 Parse Emails", type="primary", use_container_width=True)
    
    with col2:
        if st.session_state.parsed_emails:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.parsed_emails = []
                st.session_state.send_results = []
                st.rerun()
    
    if parse_button:
        if not input_text.strip():
            st.warning("⚠️ Please paste some text first")
        else:
            with st.spinner("Parsing emails..."):
                parser = EmailParser()
                valid, invalid, duplicates_info = parser.parse_and_validate(input_text)
                
                st.session_state.parsed_emails = valid
                
                if valid:
                    st.markdown(f'<div class="success-box">✓ Found {len(valid)} valid email(s)</div>', 
                               unsafe_allow_html=True)
                    
                    if invalid:
                        st.warning(f"⚠️ Filtered out {len(invalid)} invalid email(s)")
                    
                    if duplicates_info[0] != "0 duplicates removed":
                        st.info(f"ℹ️ {duplicates_info[0]}")
                else:
                    st.markdown('<div class="error-box">✗ No valid emails found</div>', 
                               unsafe_allow_html=True)
    
    # ========================================================================
    # STEP 3: REVIEW EMAILS
    # ========================================================================
    
    if st.session_state.parsed_emails:
        st.markdown("---")
        st.markdown("### 📋 Step 2: Review Extracted Emails")
        
        display_email_list(st.session_state.parsed_emails)
        
        # ====================================================================
        # STEP 4: SEND EMAILS
        # ====================================================================
        
        st.markdown("---")
        st.markdown("### 🚀 Step 3: Send Emails")
        
        # Email preview
        with st.expander("📧 Preview Email Content", expanded=False):
            st.markdown(f"**Subject:** Application for {config.JOB_TITLE} Position")
            st.markdown("**Body:**")
            
            # Load and display cover letter
            try:
                with open(config.COVER_LETTER_PATH, 'r') as f:
                    cover_letter = f.read()
                    # Replace placeholders
                    cover_letter = cover_letter.replace("{job_title}", config.JOB_TITLE)
                    cover_letter = cover_letter.replace("{company_preference}", config.COMPANY_PREFERENCE)
                    cover_letter = cover_letter.replace("{sender_name}", config.SENDER_NAME)
                    st.text(cover_letter)
            except Exception as e:
                st.error(f"Could not load cover letter: {e}")
            
            # Show which CV will be attached
            if st.session_state.uploaded_cv is not None:
                st.markdown(f"**Attachment:** {st.session_state.uploaded_cv.name} (uploaded)")
            else:
                st.markdown(f"**Attachment:** {Path(config.CV_PATH).name} (default)")
        
        # Send button
        send_button = st.button(
            f"📤 Send to {len(st.session_state.parsed_emails)} Recipient(s)",
            type="secondary",
            use_container_width=True,
            disabled=st.session_state.is_sending
        )
        
        if send_button:
            st.session_state.is_sending = True
            st.session_state.send_results = []
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            results_container = st.container()
            
            # Initialize sender
            sender = EmailSender()
            
            # Progress callback
            def update_progress(current: int, total: int, result: EmailSendResult):
                progress = current / total
                progress_bar.progress(progress)
                
                status_icon = "✓" if result.success else "✗"
                status_text.markdown(
                    f"**{status_icon} Sending {current}/{total}:** {result.email}"
                )
                
                # Store result
                st.session_state.send_results.append(result)
            
            # Send emails
            try:
                # Get uploaded CV data if available
                uploaded_cv_bytes = None
                uploaded_cv_name = None
                if st.session_state.uploaded_cv is not None:
                    uploaded_cv_bytes = st.session_state.uploaded_cv.getvalue()
                    uploaded_cv_name = st.session_state.uploaded_cv.name
                
                results = sender.send_bulk_emails(
                    recipient_emails=st.session_state.parsed_emails,
                    progress_callback=update_progress,
                    uploaded_cv_bytes=uploaded_cv_bytes,
                    uploaded_cv_name=uploaded_cv_name
                )
                
                # Complete
                progress_bar.progress(1.0)
                status_text.empty()
                
                st.markdown('<div class="success-box">✓ Bulk send completed!</div>', 
                           unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f'<div class="error-box">✗ Error: {str(e)}</div>', 
                           unsafe_allow_html=True)
            
            finally:
                st.session_state.is_sending = False
    
    # ========================================================================
    # STEP 5: SHOW RESULTS
    # ========================================================================
    
    if st.session_state.send_results:
        st.markdown("---")
        st.markdown("### 📊 Results Summary")
        
        display_metrics(st.session_state.send_results)
        
        # Detailed results
        with st.expander("📝 Detailed Results", expanded=False):
            for result in st.session_state.send_results:
                if result.success:
                    st.success(f"✓ {result.email}")
                else:
                    st.error(f"✗ {result.email} - {result.error}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.85rem; padding: 2rem 0;">
        <p>💡 <strong>Tip:</strong> For best results on mobile, use landscape orientation</p>
        <p>🔒 Your credentials are secure and never exposed to the frontend</p>
        <p style="margin-top: 1rem; opacity: 0.7;">Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
