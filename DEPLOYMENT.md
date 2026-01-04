# 🚀 Deployment Guide - Streamlit Community Cloud

Follow these steps to deploy your Bulk Email Sender app for FREE on Streamlit Cloud.

## 📋 Prerequisites

1. ✅ GitHub account (you already have this)
2. ✅ Code pushed to GitHub repository (done!)
3. 📧 Gmail account with App Password

---

## 🔐 Step 1: Get Gmail App Password

Before deploying, you need a Gmail App Password:

1. **Enable 2-Factor Authentication**:
   - Go to https://myaccount.google.com/security
   - Click "2-Step Verification" and follow the setup

2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "Streamlit Email App"
   - Click "Generate"
   - **SAVE THIS PASSWORD** - you'll need it in Step 3!

---

## 🌐 Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit: https://share.streamlit.io
   - Click "Sign in" → "Continue with GitHub"
   - Authorize Streamlit to access your GitHub

2. **Create New App**:
   - Click "New app" button
   - Select your repository: `Shreyyyyy/automating_job_email`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy"!

---

## 🔑 Step 3: Add Secrets (IMPORTANT!)

After deployment starts, you need to add your credentials:

1. **Open App Settings**:
   - Click the "⋮" menu on your app
   - Select "Settings"
   - Go to "Secrets" tab

2. **Add Your Secrets**:
   Copy and paste this template, then fill in YOUR values:

```toml
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-16-char-app-password"
SENDER_NAME = "Your Full Name"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "587"
JOB_TITLE = "Software Engineer"
COMPANY_PREFERENCE = "innovative tech companies"
MIN_DELAY = "10"
MAX_DELAY = "15"
```

3. **Click "Save"**
   - The app will automatically restart with your secrets

---

## ✅ Step 4: Test Your App

1. Wait for deployment to complete (usually 1-2 minutes)
2. You'll get a URL like: `https://your-app-name.streamlit.app`
3. Open it on your phone browser!
4. Test by:
   - Pasting some text with emails
   - Uploading a CV
   - Sending a test email to yourself

---

## 📱 Step 5: Use from Your Phone

1. **Bookmark the URL** on your phone's home screen:
   - **iPhone**: Safari → Share → "Add to Home Screen"
   - **Android**: Chrome → Menu → "Add to Home Screen"

2. **Use it anywhere**:
   - Open the app from your home screen
   - Works like a native app!
   - No installation needed

---

## 🔒 Security Notes

- ✅ Your credentials are stored securely in Streamlit Cloud
- ✅ Never shared or exposed to users
- ✅ App uses SMTP with TLS encryption
- ✅ Rate limiting prevents spam blocking
- ✅ `.env` and `cv.pdf` are in `.gitignore` (not on GitHub)

---

## 🛠️ Troubleshooting

### App won't start?
- Check that all secrets are added correctly
- Make sure there are no extra spaces in secret values
- Verify your Gmail App Password is correct

### Emails not sending?
- Verify Gmail App Password (not regular password!)
- Check that 2FA is enabled on your Gmail
- Try sending to yourself first as a test

### App is slow?
- Free tier has limited resources
- Consider upgrading if you send many emails
- Rate limiting helps prevent issues

---

## 🎉 You're Done!

Your app is now live and accessible from anywhere! 

**Your app URL**: Check Streamlit Cloud dashboard

Share it with friends or keep it private - it's your choice!

---

## 💡 Tips

- **Update the app**: Just push to GitHub, it auto-deploys!
- **Monitor usage**: Check Streamlit Cloud dashboard for stats
- **Keep it free**: Stay within free tier limits
- **Mobile first**: Designed for phone use, but works on desktop too!

---

Need help? Check the [Streamlit Community Forum](https://discuss.streamlit.io/)
