# 🚀 Deploy CultureExplore to Vercel

Follow this guide to get your app running on Vercel with a free PostgreSQL database.

---

## Step 1: Get a Free PostgreSQL Database (Neon - Recommended)

You **must** use PostgreSQL on Vercel. SQLite will not work because serverless functions cannot persist files.

### Option A: Neon (Easiest)

1. Go to **https://neon.tech**
2. Sign up with Google or GitHub
3. Click **"Create Project"**
   - Project name: `cultureexplore`
   - PostgreSQL version: 15
   - Region: Choose closest to you (e.g., `US East`)
   - Click **"Create Project"**
4. On the dashboard, you'll see a connection string like:
   ```
   postgresql://username:password@ep-cool-name.us-east-1.aws.neon.tech/dbname?sslmode=require
   ```
5. Click the **copy icon** next to the connection string

### Option B: Supabase

1. Go to **https://supabase.com**
2. Sign up and click **"New Project"**
3. Set a strong database password and **save it!**
4. Once created, click **"Connect"** → **"URI"** tab
5. Copy the connection string (replace `[YOUR-PASSWORD]` with your actual password)

---

## Step 2: Generate a SECRET_KEY

1. Go to **https://randomkeygen.com**
2. Copy a random key (e.g., from the "CodeIgniter Encryption Keys" section)
3. Save it — you'll paste it in Vercel next

---

## Step 3: Add Environment Variables in Vercel

1. Go to **https://vercel.com** and sign in
2. Import your GitHub repository (`Xamuel12/data-mining`)
3. Before clicking **Deploy**, click on **"Environment Variables"**
4. Add these two variables:

| Variable       | Value                                        |
| -------------- | -------------------------------------------- |
| `SECRET_KEY`   | (paste the random key from Step 2)           |
| `DATABASE_URL` | (paste the Neon/Supabase string from Step 1) |
| `FLASK_ENV`    | `production`                                 |

5. Click **Deploy**

---

## Step 4: Wait for Deployment

- Vercel will build and deploy your app
- This may take 2–5 minutes the first time
- Once done, you'll get a live URL like `https://cultureexplore.vercel.app`

---

## Step 5: Test Signup

1. Visit your live URL
2. Go to **Sign Up**
3. Create an account
4. If it fails, check the logs:
   - Vercel Dashboard → Your Project → **Deployments** → Click latest → **Logs**

---

## ⚠️ Important Notes

### Size Limit Warning

Vercel has a **50MB serverless function size limit**. Your app uses:

- pandas
- scikit-learn
- numpy

These are large libraries. If deployment fails with a "Function size too large" error, you have two options:

#### Option 1: Reduce requirements (if you don't need all algorithms)

Edit `requirements.txt` and remove unused libraries. If you only need K-Means, you can minimize.

#### Option 2: Use an alternative free host

| Platform           | Why Use It?                    | Link                       |
| ------------------ | ------------------------------ | -------------------------- |
| **Koyeb**          | Docker support, no cold starts | https://koyeb.com          |
| **Railway**        | Generous free tier             | https://railway.app        |
| **PythonAnywhere** | Free tier available            | https://pythonanywhere.com |

---

## 🔧 Troubleshooting

### "Internal Server Error" on Signup

- Check Vercel logs for the exact error
- Most common cause: `DATABASE_URL` is missing or incorrect
- Make sure the database connection string includes the correct password

### "Database connection failed"

- Verify your `DATABASE_URL` has no spaces
- Make sure the database server is running (check Neon/Supabase dashboard)
- Ensure the connection string starts with `postgresql://` or `postgres://`

### "Module not found" errors

- Make sure all libraries in `requirements.txt` are spelled correctly
- Vercel uses Python 3.9 by default. If you need 3.11, add `PYTHON_VERSION=3.11` as an env var

---

## 🎯 Quick Checklist

- [ ] Got PostgreSQL connection string from Neon or Supabase
- [ ] Generated a random SECRET_KEY
- [ ] Added both as Environment Variables in Vercel
- [ ] Clicked Deploy
- [ ] Tested signup on the live URL

---

## 📞 Still Stuck?

If you keep getting errors, check the **Logs** tab in Vercel. Look for lines that say:

```
SIGNUP ERROR: ...
```

Those messages will tell you exactly what's wrong.
