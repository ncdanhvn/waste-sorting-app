#!/bin/bash

echo "==========================================="
echo "Waste Sorting App - Deployment Setup"
echo "==========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi

echo ""
echo "Checking files to be committed..."
git add .
git status

echo ""
echo "==========================================="
echo "Next Steps:"
echo "==========================================="
echo ""
echo "1. Create a GitHub repository:"
echo "   - Go to: https://github.com/new"
echo "   - Name: waste-sorting-app"
echo "   - Keep it Public"
echo "   - Don't initialize with README"
echo ""
echo "2. Commit your code:"
echo "   git commit -m \"Initial commit - AI Waste Sorting App\""
echo ""
echo "3. Add remote (replace YOUR_USERNAME):"
echo "   git remote add origin https://github.com/YOUR_USERNAME/waste-sorting-app.git"
echo ""
echo "4. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "5. Deploy to Render.com:"
echo "   - Go to: https://render.com"
echo "   - Sign up with GitHub"
echo "   - Create New Web Service"
echo "   - Connect your repository"
echo "   - Add ANTHROPIC_API_KEY environment variable"
echo "   - Deploy!"
echo ""
echo "For detailed instructions, see DEPLOYMENT.md"
echo "==========================================="
