# Deploying Waste Sorting App Online (Free)

This guide will help you deploy the waste sorting app online for free using Render.com. The deployed app will have HTTPS enabled automatically (required for camera access).

## Option 1: Render.com (Recommended)

**Why Render:**
- ✅ Completely free tier (no credit card required)
- ✅ Automatic HTTPS/SSL
- ✅ Easy deployment from GitHub
- ✅ Perfect for Flask apps
- ✅ Always-on (doesn't sleep on free tier)

### Prerequisites

1. A GitHub account
2. Git installed on your computer
3. Your Anthropic API key

### Step-by-Step Guide

#### 1. Push Your Code to GitHub

First, initialize git and push your code to GitHub:

```bash
cd /home/danny/repos/waste-sorting-app

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - AI Waste Sorting App"

# Create a new repository on GitHub (do this in your browser):
# Go to https://github.com/new
# Name it: waste-sorting-app
# Keep it public
# Don't initialize with README (we already have code)

# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/waste-sorting-app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### 2. Sign Up for Render

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with your GitHub account (easiest option)
4. Authorize Render to access your repositories

#### 3. Create a New Web Service

1. From Render Dashboard, click "New +" button
2. Select "Web Service"
3. Connect your GitHub repository:
   - Click "Connect account" if not connected
   - Find and select `waste-sorting-app` repository
4. Click "Connect"

#### 4. Configure Your Service

Fill in the following settings:

- **Name:** `waste-sorting-app` (or any name you prefer)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

#### 5. Add Environment Variables

Scroll down to "Environment Variables" section:

1. Click "Add Environment Variable"
2. Add the following:
   - **Key:** `ANTHROPIC_API_KEY`
   - **Value:** Your actual Anthropic API key (paste it here)

#### 6. Deploy!

1. Scroll down and click "Create Web Service"
2. Wait for deployment (usually 2-5 minutes)
3. Watch the logs for any errors

#### 7. Access Your App

Once deployed, Render will give you a URL like:
```
https://waste-sorting-app-xxxx.onrender.com
```

Open this URL in your browser - your app is now live online! 🎉

### Testing Your Deployed App

1. Open the URL in your mobile browser
2. Allow camera access when prompted
3. Take a photo of waste
4. Analyze it with AI

**Note:** HTTPS is automatically enabled on Render, so camera access will work!

---

## Option 2: Railway.app (Alternative)

Railway offers 500 hours/month free, which is enough for testing.

### Steps:

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `waste-sorting-app` repository
5. Add environment variable:
   - `ANTHROPIC_API_KEY`: Your API key
6. Railway will auto-detect it's a Python app and deploy
7. Click "Generate Domain" to get a public URL

---

## Option 3: PythonAnywhere (Alternative)

PythonAnywhere offers a free tier with some limitations.

### Steps:

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Go to "Web" tab
3. Click "Add a new web app"
4. Choose "Manual configuration" → Python 3.10
5. Upload your code via Files tab or git clone
6. Configure WSGI file to point to your app
7. Set ANTHROPIC_API_KEY in .env file
8. Reload web app

**Limitation:** Free tier doesn't support HTTPS for custom domains, but works on their subdomain.

---

## Troubleshooting

### Deployment Fails

**Check the logs** in Render dashboard. Common issues:

1. **Missing dependencies:** Make sure `requirements.txt` is correct
2. **API key not set:** Verify environment variable is set correctly
3. **Port binding:** Render sets `PORT` env variable automatically - gunicorn handles this

### App is Slow

Free tier services may have cold starts:
- First request after idle may take 30-60 seconds
- Subsequent requests are fast

### Camera Not Working

Make sure you're accessing via HTTPS:
- ✅ `https://your-app.onrender.com`
- ❌ `http://your-app.onrender.com`

Render provides HTTPS automatically.

### API Rate Limits

The free app might hit Anthropic API rate limits if many people use it. Consider:
- Adding rate limiting on your app
- Using a paid Anthropic plan for higher limits

---

## Cost Considerations

### Render.com Free Tier

- **Included:**
  - 750 hours/month (enough for always-on app)
  - Automatic SSL
  - Custom domains
  - 512 MB RAM
  - Shared CPU

- **Limitations:**
  - Services spin down after 15 min of inactivity
  - Limited to 100 GB bandwidth/month
  - Slower cold starts

### Upgrading (Optional)

If you need better performance:
- **Render Starter ($7/month):** Always-on, no cold starts
- **Railway ($5/month):** More flexible usage

---

## Next Steps After Deployment

1. **Custom Domain (Optional):**
   - Buy a domain (Namecheap, Google Domains)
   - Add custom domain in Render dashboard
   - Update DNS records

2. **Monitoring:**
   - Check Render logs for errors
   - Monitor API usage in Anthropic dashboard

3. **Share:**
   - Share your URL with friends
   - Add to your portfolio
   - Tweet about it!

4. **Improvements:**
   - Add analytics (Google Analytics)
   - Add user feedback form
   - Track classification accuracy

---

## Security Notes

- ✅ Never commit `.env` file to GitHub (already in `.gitignore`)
- ✅ Use environment variables for API keys
- ✅ Render encrypts environment variables
- ✅ HTTPS is enforced automatically

---

## Support

If you encounter issues:
1. Check Render documentation: [render.com/docs](https://render.com/docs)
2. Check deployment logs in Render dashboard
3. Verify environment variables are set correctly
4. Make sure your Anthropic API key has sufficient credits

---

## Files Added for Deployment

- `requirements.txt` - Added gunicorn for production server
- `render.yaml` - Render configuration (optional, auto-detected)
- `Procfile` - Process file for service detection
- `runtime.txt` - Python version specification
- `DEPLOYMENT.md` - This file

Your app is ready to deploy! 🚀
