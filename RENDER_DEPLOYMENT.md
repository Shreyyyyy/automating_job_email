# 🚀 Deploy to Render (Free)

This guide will help you deploy your Bulk Email Sender app to Render's free tier.

## Why Render?

- ✅ **Free tier** with 750 hours/month (enough for continuous running)
- ✅ **No credit card required** for free tier
- ✅ **Automatic HTTPS** with custom domains
- ✅ **Easy deployment** from GitHub
- ✅ **Environment variables** support
- ✅ **Auto-deploy** on git push

## 📋 Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Gmail App Password** - For sending emails (see below)
3. **Render Account** - Sign up at [render.com](https://render.com) (free)

## 🔐 Step 1: Get Gmail App Password

1. Enable **2-Factor Authentication** on your Gmail account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Navigate to: **Security** → **2-Step Verification** → **App passwords**
4. Generate an app password for "Mail"
5. **Save this password** - you'll need it for Render

## 📤 Step 2: Push to GitHub

If you haven't already:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit for Render deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## 🌐 Step 3: Deploy to Render

### Option A: Deploy with Blueprint (Recommended)

1. **Sign up/Login** to [Render](https://render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**
6. Set the following **Environment Variables**:
   - `SENDER_EMAIL`: Your Gmail address (e.g., `yourname@gmail.com`)
   - `SENDER_PASSWORD`: Your Gmail App Password (16-character code)
   - `SENDER_NAME`: Your full name
   - `JOB_TITLE`: Job title you're applying for (e.g., `Software Engineer`)
   - `COMPANY_PREFERENCE`: Type of companies (e.g., `innovative tech companies`)

### Option B: Manual Deployment

1. **Sign up/Login** to [Render](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `bulk-email-sender` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - **Instance Type**: `Free`

5. Add **Environment Variables** (click "Advanced" → "Add Environment Variable"):
   ```
   SENDER_EMAIL = your-email@gmail.com
   SENDER_PASSWORD = your-app-password-here
   SENDER_NAME = Your Full Name
   SMTP_HOST = smtp.gmail.com
   SMTP_PORT = 587
   JOB_TITLE = Software Engineer
   COMPANY_PREFERENCE = innovative tech companies
   ```

6. Click **"Create Web Service"**

## ⏱️ Step 4: Wait for Deployment

- Render will build and deploy your app (takes 2-5 minutes)
- You'll see build logs in real-time
- Once deployed, you'll get a URL like: `https://bulk-email-sender.onrender.com`

## ✅ Step 5: Test Your App

1. Open your Render URL
2. Upload a CV or use the default
3. Paste some text with email addresses
4. Click "Parse Emails"
5. Send a test email!

## 📱 Mobile Access

Your app is now accessible from anywhere:
- Desktop: Open the Render URL in any browser
- Mobile: Save the URL to your home screen for app-like experience

## 🔄 Auto-Deploy Updates

Every time you push to GitHub, Render will automatically redeploy:

```bash
git add .
git commit -m "Update app"
git push
```

## ⚠️ Important Notes

### Free Tier Limitations

- **Spins down after 15 minutes** of inactivity
- **First request after spin-down** takes 30-60 seconds (cold start)
- **750 hours/month** free (enough for continuous use)
- **No custom domain** on free tier (use `.onrender.com` subdomain)

### Keeping Your App Awake (Optional)

To prevent spin-down, you can use a free uptime monitor:
- [UptimeRobot](https://uptimerobot.com) - Ping your app every 5 minutes
- [Cron-Job.org](https://cron-job.org) - Schedule HTTP requests

### Security Best Practices

1. **Never commit** `.env` file (already in `.gitignore`)
2. **Use environment variables** for all secrets
3. **Rotate app passwords** periodically
4. **Monitor usage** to avoid hitting Gmail's sending limits

## 🆘 Troubleshooting

### App Won't Start
- Check build logs in Render dashboard
- Verify all environment variables are set correctly
- Ensure `requirements.txt` is up to date

### Email Sending Fails
- Verify Gmail App Password is correct (16 characters, no spaces)
- Check that 2FA is enabled on your Gmail account
- Ensure `SENDER_EMAIL` matches the Gmail account

### App is Slow
- Free tier spins down after inactivity (normal behavior)
- First request after spin-down takes 30-60 seconds
- Consider using an uptime monitor to keep it awake

### Build Fails
- Check Python version compatibility
- Verify all dependencies in `requirements.txt`
- Review build logs for specific errors

## 🎉 Success!

Your bulk email sender is now deployed and accessible from anywhere! 

**Your App URL**: `https://YOUR-APP-NAME.onrender.com`

Share this URL with anyone who needs to send bulk emails, or save it to your phone's home screen for quick access.

## 🔗 Useful Links

- [Render Dashboard](https://dashboard.render.com)
- [Render Documentation](https://render.com/docs)
- [Gmail App Passwords](https://myaccount.google.com/apppasswords)
- [GitHub Repository](https://github.com)

---

**Need Help?** Check the Render logs in your dashboard for detailed error messages.
