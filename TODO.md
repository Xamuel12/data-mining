# Fix Signup & Deploy to Vercel - TODO

## Steps

- [x] 1. Read and analyze all relevant files (app.py, vercel.json, render.yaml, requirements.txt, signup.html, init_db.py, DEPLOYMENT_GUIDE.md)
- [x] 2. Fix app.py — Add try/except with db.session.rollback() on signup/login, better init_db error handling, SQLite /tmp fallback
- [x] 3. Update vercel.json — Add excludeFiles to reduce bundle size, optimize for serverless
- [x] 4. Create .env.example — Template for DATABASE_URL and SECRET_KEY
- [x] 5. Create VERCEL_SETUP.md — Step-by-step deployment guide (Neon/Supabase DB + Vercel env vars)
- [x] 6. Create api/index.py — Alternative Vercel entry point for better serverless compatibility
- [x] 7. Test app.py syntax (quick sanity check)
- [x] 8. Provide final deployment instructions

## Notes

- Root cause of signup internal error: No try/except around db.session.commit() — any DB failure crashes Flask with 500. Now fixed with rollback and user-friendly error messages.
- Vercel has 50MB function size limit; ML libs may exceed it. Fallback options: Koyeb, Railway, PythonAnywhere
- Must use PostgreSQL on Vercel (SQLite won't persist across serverless invocations)
