# Quick Deployment Guide (5 Minutes)

The fastest way to get your app online for free!

## Step 1: Push to GitHub (2 minutes)

```bash
# In your project directory
./deploy_setup.sh

# Follow the on-screen instructions to:
# 1. Create GitHub repo at https://github.com/new
# 2. Commit your code
# 3. Push to GitHub
```

Or manually:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/waste-sorting-app.git
git push -u origin main
```

## Step 2: Deploy on Render (3 minutes)

1. Go to [render.com](https://render.com) → Sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect your `waste-sorting-app` repository
4. Fill in:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Add Environment Variable:
   - **Key:** `ANTHROPIC_API_KEY`
   - **Value:** Your Anthropic API key
6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment

## Step 3: Test Your App

1. Open the URL provided by Render (e.g., `https://waste-sorting-app-xxxx.onrender.com`)
2. Allow camera access
3. Take a photo of waste
4. Click "Analyze Waste"
5. See results! 🎉

## Troubleshooting

**Deployment failed?**
- Check logs in Render dashboard
- Verify API key is set correctly

**Camera not working?**
- Make sure you're using HTTPS (Render provides this automatically)
- Allow camera permissions in browser

**App is slow on first request?**
- Free tier apps "spin down" after inactivity
- First request wakes them up (takes ~30 seconds)
- Subsequent requests are fast

## What's Next?

- Share your URL with friends!
- Add it to your portfolio
- Update the README.md with your live URL
- Consider upgrading to paid tier for better performance ($7/month)

For detailed deployment options and troubleshooting, see [DEPLOYMENT.md](DEPLOYMENT.md)
