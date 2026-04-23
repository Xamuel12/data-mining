# 🌍 CultureExplore

**Data Mining Platform for Cultural Heritage Analysis**

Analyzing over **270 towns** across **20 LGAs** in Ogun State, Nigeria using machine learning clustering (K-Means, DBSCAN, Hierarchical) to uncover patterns in food, clothing, dance, religion, and traditions.

---

## 🚀 Quick Deploy

### Option 1: Vercel (Serverless)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Add Environment Variables (see below)
4. Click **Deploy**

> ⚠️ **Note:** Vercel has a 50MB serverless function size limit. The ML libraries (pandas, scikit-learn, numpy) may exceed this. If deployment fails, use **Option 2: Render**.

### Option 2: Render (Recommended for ML Apps)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Fork this repo to your GitHub
2. Click the button above or go to [render.com](https://render.com)
3. Create a new **Web Service**
4. Connect your GitHub repo
5. Add Environment Variables
6. Deploy

---

## 🔧 Environment Variables

| Variable       | Required | Description                                                                                                  |
| -------------- | -------- | ------------------------------------------------------------------------------------------------------------ |
| `SECRET_KEY`   | ✅ Yes   | Random string for Flask sessions. Generate one at [randomkeygen.com](https://randomkeygen.com)               |
| `DATABASE_URL` | ✅ Yes   | PostgreSQL connection string. Get free DB from [Neon](https://neon.tech) or [Supabase](https://supabase.com) |

### PostgreSQL URL Format

```
postgresql://username:password@hostname:port/database_name
```

### Example `.env` file

```env
SECRET_KEY=your-super-secret-random-key-here
DATABASE_URL=postgresql://user:pass@ep-cool-name.us-east-1.aws.neon.tech/dbname
```

---

## 🗄️ Database Setup

### Option A: Neon PostgreSQL (Free Tier)

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Paste it as `DATABASE_URL` in your deployment platform

### Option B: Supabase (Free Tier)

1. Sign up at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings → Database → Connection String
4. Copy the URI and paste as `DATABASE_URL`

---

## 🏠 Local Development

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/data-mining.git
cd data-mining

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env and add your SECRET_KEY

# 5. Run the app
python app.py
```

Visit `http://localhost:5000`

---

## 📊 Features

- 🔐 User Authentication (Register/Login/Logout)
- 🤖 K-Means Clustering
- 🤖 DBSCAN Clustering
- 🤖 Hierarchical Clustering
- 📈 Interactive Charts (Chart.js)
- 📥 Download Clustered Data as CSV
- 📱 Responsive Design
- 🎨 Dark Theme UI

---

## 📁 Project Structure

```
.
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel deployment config
├── .env.example           # Environment variables template
├── data/
│   └── riye_dataset_clean.csv  # Cultural dataset
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
└── templates/
    ├── layout.html
    ├── index.html
    ├── login.html
    ├── signup.html
    └── data_mining.html
```

---

## 🔗 Live Demo

**Coming soon after deployment...**

---

## 🛠️ Tech Stack

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Frontend:** Bootstrap 5, Chart.js
- **ML:** scikit-learn, pandas, numpy
- **Database:** PostgreSQL (production), SQLite (local)
- **Deployment:** Vercel / Render

---

## 📄 License

MIT License - feel free to use and modify.
