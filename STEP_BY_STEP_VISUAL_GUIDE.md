# Render.com Deployment - Step by Step Visual Guide

## STEP 1: Generate SECRET_KEY for Django

Open PowerShell and run:
```powershell
cd C:\Users\manve\Desktop\Student tracking\backend
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Output**: Copy the generated string (looks like: `abc123xyz...`)
**Save this**: You'll need it in Step 3

---

## STEP 2: Create PostgreSQL Database on Render

### 2.1 Go to Render Dashboard
- URL: https://dashboard.render.com
- Sign up / Log in

### 2.2 Create New PostgreSQL
```
Dashboard → New + → PostgreSQL
```

### 2.3 Fill in Form
```
Name: student-tracking-db
Database: student_tracking
User: (auto-generated)
Region: (choose closest)
Plan: Free
```

### 2.4 Click "Create Database"
- Wait 1-2 minutes for creation
- You'll see the database details page

### 2.5 Copy External Database URL
```
Look for: External Database URL
Example: postgresql://user:password@host.onrender.com:5432/database
Save this in notepad - you'll need it in Step 3
```

---

## STEP 3: Deploy Backend to Render

### 3.1 Create Web Service
```
Dashboard → New + → Web Service
```

### 3.2 Connect GitHub
```
Select: Your GitHub repository
(Must be pushed to GitHub)
```

### 3.3 Configure Service
```
Name: student-tracking-backend
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn backend.wsgi:application
Plan: Free
Region: (same as database)
```

### 3.4 Click "Create Web Service"
- Service will start deploying
- Wait 5-15 minutes

### 3.5 Add Environment Variables
While waiting, go to **Environment** tab and add:

```
DEBUG = False
SECRET_KEY = (paste from STEP 1)
DATABASE_URL = (paste from STEP 2)
ALLOWED_HOSTS = student-tracking-backend.onrender.com
CORS_ALLOWED_ORIGINS = https://student-tracking-frontend.onrender.com
FRONTEND_BASE_URL = https://student-tracking-frontend.onrender.com
FRONTEND_URL = https://student-tracking-frontend.onrender.com
EMAIL_HOST_USER = your_gmail@gmail.com
EMAIL_HOST_PASSWORD = (Gmail app password - see instructions)
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = your_gmail@gmail.com
```

### 3.6 Save & Deploy
- Click "Save Changes"
- Service will restart with new variables
- Check **Logs** tab for errors
- ✅ Backend should be running

### 3.7 Test Backend
Open browser and go to:
```
https://student-tracking-backend.onrender.com/api/users/
(Should see a JSON response or 401 error - that's good!)
```

---

## STEP 4: Deploy Frontend to Render

### 4.1 Create Static Site
```
Dashboard → New + → Static Site
```

### 4.2 Connect GitHub
```
Select: Your GitHub repository
(Same repo as backend, just frontend folder)
```

### 4.3 Configure Service
```
Name: student-tracking-frontend
Build Command: npm install && npm run build
Publish Directory: dist
Plan: Free
Region: (same as backend)
```

### 4.4 Click "Create Static Site"
- Service will start deploying
- Wait 3-10 minutes

### 4.5 Add Environment Variables
Go to **Environment** tab and add:

```
VITE_API_BASE_URL = https://student-tracking-backend.onrender.com
VITE_API_TIMEOUT = 30000
VITE_APP_NAME = Student Tracking Platform
```

### 4.6 Save & Redeploy
- Click "Save Changes"
- Service will rebuild and redeploy
- ✅ Frontend should be running

---

## STEP 5: Test Everything

### 5.1 Test Backend
Go to:
```
https://student-tracking-backend.onrender.com/api/users/
```

Expected:
- ✅ Page loads (JSON or 401 error means it's working)
- ❌ Page not found / error means something's wrong

### 5.2 Test Frontend
Go to:
```
https://student-tracking-frontend.onrender.com
```

Expected:
- ✅ App loads, can see login page
- ❌ Blank page / errors in console means check logs

### 5.3 Test Login
1. Try to login with a test user
2. Should connect to backend
3. Check browser console (F12) for errors

### 5.4 Check Logs for Errors
If something doesn't work:

**Backend Logs:**
```
Dashboard → Backend Service → Logs
Look for any RED error messages
```

**Frontend Logs:**
```
Dashboard → Frontend Service → Logs
Look for any build errors
```

---

## 📧 Gmail App Password Setup (If needed)

1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification (if not already on)
3. Find "App passwords" section
4. Select Mail and Windows
5. Google gives you 16-character password
6. Use this as `EMAIL_HOST_PASSWORD` in Render

---

## 🔄 Making Updates After Deployment

### To update Backend:
```powershell
cd c:\Users\manve\Desktop\Student tracking
git add .
git commit -m "Backend updates"
git push origin main
```
**Render will auto-deploy** (5-10 minutes)

### To update Frontend:
```powershell
cd c:\Users\manve\Desktop\Student tracking\student-frontend
git add .
git commit -m "Frontend updates"
git push origin main
```
**Render will auto-deploy** (3-5 minutes)

---

## ❌ If Something Goes Wrong

### Backend won't start?
1. Go to **Logs** tab
2. Look for red error messages
3. Common issues:
   - Missing environment variables
   - Bad DATABASE_URL
   - Syntax error in settings.py

### Frontend is blank page?
1. Open browser Developer Tools (F12)
2. Check **Console** tab for errors
3. Check **Network** tab to see if API calls work
4. Common issues:
   - VITE_API_BASE_URL is wrong
   - Backend isn't responding
   - CORS blocked request

### Can't login / API not working?
1. Check CORS_ALLOWED_ORIGINS includes frontend domain
2. Test backend directly in browser
3. Check backend logs for errors
4. Verify email settings are correct

---

## 📊 Your Final URLs

After deployment, you'll have:

**Backend:**
```
https://student-tracking-backend.onrender.com
```

**Frontend:**
```
https://student-tracking-frontend.onrender.com
```

**Database:**
```
PostgreSQL on Render (managed)
```

---

## ✅ Deployment Checklist

- [ ] SECRET_KEY generated and saved
- [ ] PostgreSQL database created
- [ ] PostgreSQL URL copied
- [ ] Backend service created
- [ ] Backend environment variables set
- [ ] Backend is running (check logs)
- [ ] Backend is accessible via URL
- [ ] Frontend service created
- [ ] Frontend environment variables set
- [ ] Frontend is running (check logs)
- [ ] Frontend is accessible via URL
- [ ] Can login to frontend
- [ ] No errors in console/logs

---

## 🎯 Success Criteria

✅ **You're successful when:**
1. Backend URL responds in browser
2. Frontend loads without errors
3. Can login with correct credentials
4. No CORS errors in console
5. API calls work from frontend
6. Both services stay running without crashing

---

## 💡 Pro Tips

1. **Keep secrets safe**: Never commit `.env` files to GitHub
2. **Monitor logs**: Check logs regularly after deployment
3. **Use free tier first**: Start free, upgrade only if needed
4. **Back up database**: Periodically export your PostgreSQL data
5. **Test locally first**: Fix bugs locally before pushing to Render

---

**Happy Deploying! 🚀**

For detailed info, see:
- `QUICK_START_RENDER.md` - Quick reference
- `RENDER_DEPLOYMENT_GUIDE.md` - Detailed guide
- `DEPLOYMENT_SUMMARY.md` - Complete overview
