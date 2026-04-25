# Deploy CultureExplore to Render (Step-by-Step)

Follow these exact steps to deploy your app on Render with a free PostgreSQL database.

---

## Step 1: Push Your Code to GitHub

Open **CMD** (not PowerShell) and run:

```cmd
cd "c:\Users\USER\Desktop\DATA MINING"
git add app.py render.yaml
git commit -m "Fix signup error handling and session persistence for Render"
git push origin master
```

If `git push` fails, try:

```cmd
git push https://github.com/Xamuel12/data-mining.git master
```

---

## Step 2: Go to Render

1. Open **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub** account
4. Authorize Render to access your repositories

---

## Step 3: Deploy with Blueprint

1. On your Render dashboard, click **"New +"**
2. Select **"Blueprint"**
3. Find and select your **`data-mining`** repository
4. Render will detect the `render.yaml` file automatically
5. Click **"Apply"**

Render will now:

- Create a free **PostgreSQL database** automatically
- Deploy your Flask app
- Set `DATABASE_URL` and `SECRET_KEY` automatically

---

## Step 4: Wait for Deployment

This takes **3-5 minutes**. You'll see:

- Database: `cultureexplore-db` (creating...)
- Web Service: `cultureexplore` (building...)

Once both show **"Live"**, click the web service URL.

---

## Step 5: Test Your App

1. Visit your live URL (e.g., `https://cultureexplore.onrender.com`)
2. Go to **Sign Up** → create an account
3. **Log in**
4. Go to **Data Mining**
5. Switch between **K-Means**, **DBSCAN**, and **Hierarchical** — it should stay logged in

---

## Troubleshooting

### "Internal Server Error" on Signup

- Check Render dashboard → your service → **Logs**
- Look for `SIGNUP ERROR:` messages
- Most likely: Database still initializing, wait 2 minutes and retry

### App says "Build Succeeded" but won't start

- Check that `render.yaml` has `startCommand: python init_db.py && gunicorn app:app`

### Can't find my repository

- Make sure you pushed to GitHub first
- Check that your repo is public, or grant Render access to private repos

---

## Need Help?

If Render fails, the alternative is:

- **Railway**: https://railway.app (free tier, easier setup)
