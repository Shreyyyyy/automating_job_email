#!/bin/bash

# Bulk Email Sender - Quick Deployment Script
# This script helps you deploy to various platforms

set -e  # Exit on error

echo "🚀 Bulk Email Sender - Deployment Helper"
echo "========================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
    echo "✅ Git repository initialized"
    echo ""
fi

# Show deployment options
echo "Choose your deployment platform:"
echo ""
echo "1. 🟣 Render (Recommended - No credit card needed)"
echo "2. 🚂 Railway (Requires credit card)"
echo "3. ☁️  Fly.io (Requires credit card, Docker-based)"
echo "4. 🌊 Hugging Face Spaces (Free, always-on)"
echo "5. 🔷 Koyeb (No credit card needed)"
echo "6. 📖 Show all options comparison"
echo "7. ❌ Exit"
echo ""

read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo ""
        echo "🟣 Deploying to Render..."
        echo ""
        echo "📋 Next steps:"
        echo "1. Push your code to GitHub:"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
        echo "   git push -u origin main"
        echo ""
        echo "2. Go to https://render.com and sign up/login"
        echo "3. Click 'New +' → 'Blueprint'"
        echo "4. Connect your GitHub repository"
        echo "5. Render will detect render.yaml automatically"
        echo "6. Set environment variables (see RENDER_DEPLOYMENT.md)"
        echo ""
        echo "📖 Full guide: RENDER_DEPLOYMENT.md"
        ;;
    
    2)
        echo ""
        echo "🚂 Deploying to Railway..."
        echo ""
        echo "📋 Next steps:"
        echo "1. Push your code to GitHub:"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
        echo "   git push -u origin main"
        echo ""
        echo "2. Go to https://railway.app and sign up/login"
        echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
        echo "4. Select your repository"
        echo "5. Railway will auto-detect railway.json"
        echo "6. Add environment variables in Railway dashboard"
        echo ""
        echo "📖 Full guide: FREE_DEPLOYMENT_OPTIONS.md"
        ;;
    
    3)
        echo ""
        echo "☁️  Deploying to Fly.io..."
        echo ""
        
        # Check if flyctl is installed
        if ! command -v flyctl &> /dev/null; then
            echo "Installing Fly CLI..."
            curl -L https://fly.io/install.sh | sh
            echo ""
            echo "⚠️  Please restart your terminal and run this script again"
            exit 0
        fi
        
        echo "📋 Next steps:"
        echo "1. Login to Fly.io:"
        echo "   flyctl auth login"
        echo ""
        echo "2. Launch your app:"
        echo "   flyctl launch"
        echo ""
        echo "3. Set secrets:"
        echo "   flyctl secrets set SENDER_EMAIL=your@email.com"
        echo "   flyctl secrets set SENDER_PASSWORD=yourpassword"
        echo "   flyctl secrets set SENDER_NAME='Your Name'"
        echo "   flyctl secrets set JOB_TITLE='Software Engineer'"
        echo "   flyctl secrets set COMPANY_PREFERENCE='tech companies'"
        echo ""
        echo "4. Deploy:"
        echo "   flyctl deploy"
        echo ""
        echo "📖 Full guide: FREE_DEPLOYMENT_OPTIONS.md"
        ;;
    
    4)
        echo ""
        echo "🌊 Deploying to Hugging Face Spaces..."
        echo ""
        echo "📋 Next steps:"
        echo "1. Go to https://huggingface.co/spaces"
        echo "2. Click 'Create new Space'"
        echo "3. Choose 'Streamlit' as SDK"
        echo "4. Upload your files (app.py, requirements.txt, core/, templates/)"
        echo "5. Add secrets in Space settings:"
        echo "   - SENDER_EMAIL"
        echo "   - SENDER_PASSWORD"
        echo "   - SENDER_NAME"
        echo "   - JOB_TITLE"
        echo "   - COMPANY_PREFERENCE"
        echo "   - SMTP_HOST=smtp.gmail.com"
        echo "   - SMTP_PORT=587"
        echo ""
        echo "📖 Full guide: FREE_DEPLOYMENT_OPTIONS.md"
        ;;
    
    5)
        echo ""
        echo "🔷 Deploying to Koyeb..."
        echo ""
        echo "📋 Next steps:"
        echo "1. Push your code to GitHub:"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
        echo "   git push -u origin main"
        echo ""
        echo "2. Go to https://www.koyeb.com and sign up/login"
        echo "3. Click 'Create App' → 'GitHub'"
        echo "4. Select your repository"
        echo "5. Configure:"
        echo "   - Build command: pip install -r requirements.txt"
        echo "   - Run command: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0 --server.headless=true"
        echo "6. Add environment variables"
        echo ""
        echo "📖 Full guide: FREE_DEPLOYMENT_OPTIONS.md"
        ;;
    
    6)
        echo ""
        echo "📖 Opening comparison guide..."
        if command -v cat &> /dev/null; then
            cat FREE_DEPLOYMENT_OPTIONS.md
        else
            echo "Please read FREE_DEPLOYMENT_OPTIONS.md for detailed comparison"
        fi
        ;;
    
    7)
        echo ""
        echo "👋 Goodbye!"
        exit 0
        ;;
    
    *)
        echo ""
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "✅ Setup information displayed above"
echo ""
echo "📚 Additional resources:"
echo "  - RENDER_DEPLOYMENT.md - Detailed Render guide"
echo "  - FREE_DEPLOYMENT_OPTIONS.md - All platform comparisons"
echo "  - render.yaml - Render configuration"
echo "  - railway.json - Railway configuration"
echo "  - Dockerfile - Docker configuration"
echo ""
echo "🆘 Need help? Check the documentation files above!"
echo ""
