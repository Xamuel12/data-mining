# 🚀 CultureExplore - Deployment Guide

## How to Get a PostgreSQL Connection String

---

## 🟢 Option 1: Neon (Easiest - Recommended)

**Step 1:** Go to https://neon.tech and sign up with Google/GitHub.

**Step 2:** Click **"Create Project"**

- Project name: `cultureexplore`
- PostgreSQL version: 15 (default)
- Region: Pick closest to you (e.g., `US East`)
- Click **"Create Project"**

**Step 3:** On the dashboard, you'll see:

```
postgresql://username:password@ep-cool-name.us-east-1.aws.neon.tech/dbname?sslmode=require
```

**Step 4:** Click the **copy icon** next to the connection string.

**Step 5:** Paste it into your deployment platform as `DATABASE_URL`.

> ⚠️ **Important:** If using Vercel, the connection string starts with `postgres://` — your `app.py` automatically converts it to `postgresql://`, so it works either way.

---

## 🟣 Option 2: Supabase

**Step 1:** Go to https://supabase.com and sign up.

**Step 2:** Click **"New Project"**

- Name: `cultureexplore`
- Database password: Create a strong one and **save it!**
- Region: Closest to you
- Click **"Create New Project"** (takes ~2 minutes)

**Step 3:** Once created, click the **"Connect"** button (top right)

**Step 4:** Click **"URI"** tab

**Step 5:** You'll see:

```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxx.supabase.co:5432/postgres
```

**Step 6:** Replace `[YOUR-PASSWORD]` with the password you created in Step 2

**Step 7:** Copy the full string and paste as `DATABASE_URL`

---

## 🟠 Option 3: Render (Automatic - No Manual Setup!)

If you deploy using the `render.yaml` file in this repo, Render **automatically** creates a free PostgreSQL database and sets `DATABASE_URL` for you. You don't need to manually copy anything!

Steps:

1. Go to https://render.com
2. Sign up with GitHub
3. Click **"New +"** → **"Blueprint"**
4. Connect your `Xamuel12/data-mining` repo
5. Render automatically creates the database and deploys

---

## 📋 Where to Paste the Connection String

| Platform    | Location                                                                           |
| ----------- | ---------------------------------------------------------------------------------- |
| **Vercel**  | Dashboard → Your Project → Settings → Environment Variables → Add `DATABASE_URL`   |
| **Render**  | Dashboard → Your Service → Environment → Add Environment Variable → `DATABASE_URL` |
| **Railway** | Dashboard → Your Project → Variables → Add New → `DATABASE_URL`                    |

---

## 🧪 Test Your Connection String Format

Your connection string should look like this:

```
postgresql://username:password@hostname:port/database_name
```

Required parts:

- ✅ Starts with `postgresql://` (or `postgres://` - app handles conversion)
- ✅ Has username and password
- ✅ Has hostname (like `ep-xxx.neon.tech` or `db.xxx.supabase.co`)
- ✅ Has database name at the end

---

## 🔐 Required Environment Variables

| Variable       | Value Example                                   |
| -------------- | ----------------------------------------------- |
| `SECRET_KEY`   | `a-very-long-random-string-like-this-123456789` |
| `DATABASE_URL` | `postgresql://user:pass@host:5432/dbname`       |

Generate a random SECRET_KEY at: https://randomkeygen.com

---

## ⚡ Quick Deploy Checklist

- [ ] Get PostgreSQL connection string (Neon/Supabase/Render)
- [ ] Generate a random SECRET_KEY
- [ ] Add both as Environment Variables on your hosting platform
- [ ] Click Deploy!

---

## 🆘 Troubleshooting

**Error: "Database connection failed"**

- Check your DATABASE_URL has the correct password
- Make sure there are no spaces in the connection string
- Verify the database server is running (Neon/Supabase dashboard)

**Error: "SECRET_KEY not set"**

- You MUST set SECRET_KEY before deploying
- It cannot be empty

**Error on Vercel: "Function size too large"**

- Vercel has a 50MB limit for serverless functions
- ML libraries (pandas, scikit-learn, numpy) may exceed this
- **Solution:** Use Render.com instead (no size limit)
