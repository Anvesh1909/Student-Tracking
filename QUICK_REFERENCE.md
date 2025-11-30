# 🚀 RENDER DEPLOYMENT - ONE PAGE QUICK REFERENCE

## 📍 START HERE
**Read:** `STEP_BY_STEP_VISUAL_GUIDE.md` - Visual walkthrough with all steps

---

## ⚡ 5-MINUTE SUMMARY

### What was done:
✅ Django updated for production environment variables
✅ Added production dependencies (gunicorn, whitenoise, dj-database-url)
✅ Created Procfile for Render
✅ Created environment variable templates
✅ Created 6 detailed deployment guides

### What you need:
- GitHub account with code pushed
- Render.com account (free)
- Gmail account (for email notifications)

### Timeline: ~20 minutes total

---

## 🔑 Key Environment Variables (Copy/Paste)

### Backend (Set in Render Dashboard)
```
DEBUG=False
SECRET_KEY=GENERATE_THIS
DATABASE_URL=FROM_POSTGRES
ALLOWED_HOSTS=your-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.onrender.com
FRONTEND_BASE_URL=https://your-frontend.onrender.com
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
```

### Frontend (Set in Render Dashboard)
```
VITE_API_BASE_URL=https://your-backend.onrender.com
VITE_API_TIMEOUT=30000
```

---

## 📋 DEPLOYMENT STEPS

### STEP 1: Generate SECRET_KEY (2 min)
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
**→ Save the output**

### STEP 2: Create PostgreSQL on Render (3 min)
```
Render Dashboard → New + → PostgreSQL
→ Name: student-tracking-db
→ Plan: Free
→ Copy External Database URL
```

### STEP 3: Deploy Backend (10 min)
```
Render Dashboard → New + → Web Service
→ Select GitHub repo
→ Name: student-tracking-backend
→ Build: pip install -r requirements.txt
→ Start: gunicorn backend.wsgi:application
→ Plan: Free
→ Environment: Set all backend variables above
→ Create
```

### STEP 4: Deploy Frontend (5 min)
```
Render Dashboard → New + → Static Site
→ Select GitHub repo
→ Name: student-tracking-frontend
→ Build: npm install && npm run build
→ Publish: dist
→ Plan: Free
→ Environment: Set frontend variables above
→ Create
```

### STEP 5: Test (5 min)
```
1. Backend: https://your-backend.onrender.com/api/users/
   → Should respond with JSON or 401 error
   
2. Frontend: https://your-frontend.onrender.com
   → Should load login page
   
3. Login and test API calls
   → Should work without errors
```

---

## 📂 FILES CREATED

| Location | File | Purpose |
|----------|------|---------|
| `/backend/` | `Procfile` | Render configuration |
| `/backend/` | `requirements.txt` | Dependencies (UPDATED) |
| `/backend/` | `.env.example` | Template |
| `/backend/` | `.env.production` | Production setup |
| `/backend/backend/` | `settings.py` | (UPDATED) |
| `/student-frontend/` | `.env.example` | Template |
| `/student-frontend/` | `.env.production` | Production setup |
| `/` | `STEP_BY_STEP_VISUAL_GUIDE.md` | **MAIN GUIDE** ← Start here |
| `/` | `QUICK_START_RENDER.md` | Quick checklist |
| `/` | `RENDER_DEPLOYMENT_GUIDE.md` | Detailed guide |
| `/` | `DEPLOYMENT_SUMMARY.md` | Full reference |
| `/` | `INDEX_DEPLOYMENT.md` | Navigation |
| `/` | `FILES_AND_CHANGES.md` | What changed |

---

## ⚠️ COMMON MISTAKES TO AVOID

```
❌ Don't: Commit .env files to GitHub
✅ Do: Add .env to .gitignore

❌ Don't: Use DEBUG=True in production
✅ Do: Set DEBUG=False

❌ Don't: Forget DATABASE_URL
✅ Do: Copy exact PostgreSQL URL from Render

❌ Don't: Use same SECRET_KEY for multiple environments
✅ Do: Generate unique key for each

❌ Don't: Forget CORS_ALLOWED_ORIGINS
✅ Do: Set to your frontend URL exactly
```

---

## 🐛 TROUBLESHOOTING QUICK FIX

| Problem | Solution |
|---------|----------|
| Backend won't start | Check logs for missing DATABASE_URL or SECRET_KEY |
| Frontend blank page | Check browser F12 console for API errors |
| CORS errors | Verify CORS_ALLOWED_ORIGINS matches exactly |
| Static files broken | Whitenoise must be in MIDDLEWARE |
| Can't login | Check backend logs, verify email config |

---

## ✅ YOUR URLS AFTER DEPLOYMENT

```
Backend:  https://student-tracking-backend.onrender.com
Frontend: https://student-tracking-frontend.onrender.com
```

---

## 📞 NEED HELP?

1. **Getting started?**
   → Read `STEP_BY_STEP_VISUAL_GUIDE.md`

2. **Checklist?**
   → See `QUICK_START_RENDER.md`

3. **Detailed info?**
   → Check `RENDER_DEPLOYMENT_GUIDE.md`

4. **Troubleshooting?**
   → Go to `DEPLOYMENT_SUMMARY.md` → Troubleshooting section

5. **See what changed?**
   → Read `FILES_AND_CHANGES.md`

---

## 📊 DEPLOYMENT CHECKLIST

```
PREPARATION:
  [ ] Code pushed to GitHub
  [ ] Render account created
  [ ] Gmail app password generated
  [ ] SECRET_KEY generated

BACKEND DEPLOYMENT:
  [ ] PostgreSQL created
  [ ] Backend service created
  [ ] Environment variables set
  [ ] Backend is running (check logs)

FRONTEND DEPLOYMENT:
  [ ] Frontend service created
  [ ] Environment variables set
  [ ] Frontend is running (check logs)

TESTING:
  [ ] Backend URL responds
  [ ] Frontend page loads
  [ ] Can login successfully
  [ ] No console errors
```

---

## 🎯 SUCCESS = 

✅ Backend responds: `https://your-backend.onrender.com/api/users/`
✅ Frontend loads: `https://your-frontend.onrender.com`
✅ Can login with correct credentials
✅ No errors in browser console or logs

---

## 📈 NEXT STEPS AFTER DEPLOYMENT

1. **Monitor logs** - Check regularly for errors
2. **Test features** - Make sure everything works
3. **Update code** - Push to GitHub, Render auto-deploys
4. **Backup database** - Export data periodically
5. **Upgrade if needed** - Move to paid plan if free isn't enough

---

## 💡 USEFUL COMMANDS

```powershell
# Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# Create .env locally for testing
cp backend/.env.example backend/.env
# Edit .env with real values
```

---

## 🏁 FINAL CHECKLIST

Before you start deployment:

- [ ] Open `STEP_BY_STEP_VISUAL_GUIDE.md`
- [ ] Have GitHub open in browser
- [ ] Have Render.com open in browser
- [ ] Have Gmail open for app password
- [ ] Have a text editor for keeping notes
- [ ] Allocated 20-30 minutes of uninterrupted time

---

**Version**: 1.0
**Date**: November 30, 2025
**Status**: ✅ READY TO DEPLOY

👉 **NEXT: Open `STEP_BY_STEP_VISUAL_GUIDE.md`**

---
