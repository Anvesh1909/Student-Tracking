# Render.com Deployment Quick Start

## 🚀 5-Step Deployment Process

### Step 1: Prepare Your GitHub Repository

```bash
# Push your code to GitHub
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Set Up Backend on Render

#### Create PostgreSQL Database
1. Go to https://dashboard.render.com
2. Click **New +** → **PostgreSQL**
3. Set these values:
   - **Name**: `student-tracking-db`
   - **Database**: `student_tracking`
   - **User**: `student_tracking` (auto-generated)
   - **Plan**: Free (or Paid)
4. Click **Create Database**
5. **COPY the External Database URL** - you'll need this in Step 3

#### Deploy Backend Service
1. In Render Dashboard, click **New +** → **Web Service**
2. Select your GitHub repository
3. Configure:
   ```
   Name: student-tracking-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn backend.wsgi:application
   Plan: Free (or Paid)
   ```
4. Click **Create Web Service**
5. Go to **Environment** tab and add these variables:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | *Generate using: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`* |
| `DATABASE_URL` | *Paste PostgreSQL URL from Step 2* |
| `ALLOWED_HOSTS` | `student-tracking-backend.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | `https://student-tracking-frontend.onrender.com` |
| `FRONTEND_BASE_URL` | `https://student-tracking-frontend.onrender.com` |
| `EMAIL_HOST_USER` | *Your Gmail address* |
| `EMAIL_HOST_PASSWORD` | *Gmail app-specific password* |
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |

6. **Save environment variables**
7. **Wait for deployment** (5-15 minutes)
8. Once deployed, you'll see a URL like: `https://student-tracking-backend.onrender.com`

### Step 3: Set Up Frontend on Render

1. In Render Dashboard, click **New +** → **Static Site**
2. Select your GitHub repository
3. Configure:
   ```
   Name: student-tracking-frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
   Plan: Free
   ```
4. Click **Create Static Site**
5. Go to **Environment** tab and add:

| Key | Value |
|-----|-------|
| `VITE_API_BASE_URL` | `https://student-tracking-backend.onrender.com` |
| `VITE_API_TIMEOUT` | `30000` |

6. **Save environment variables**
7. **Wait for deployment** (3-10 minutes)
8. You'll get a URL like: `https://student-tracking-frontend.onrender.com`

### Step 4: Verify Deployment

Test these URLs in your browser:
- **Backend Health Check**: `https://student-tracking-backend.onrender.com/api/users/` (should return 401 or some response)
- **Frontend**: `https://student-tracking-frontend.onrender.com` (should load the app)

Check for errors:
- **Backend logs**: Render Dashboard → Backend Service → **Logs**
- **Frontend logs**: Render Dashboard → Frontend Service → **Logs**

### Step 5: Update Frontend API URL (If not using env vars)

If your frontend isn't picking up the environment variable, update `src/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://student-tracking-backend.onrender.com';
```

---

## 📋 Environment Variables Checklist

### Backend (.env)
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY=<generated-key>`
- [ ] `DATABASE_URL=<postgresql-url>`
- [ ] `ALLOWED_HOSTS=your-backend.onrender.com`
- [ ] `CORS_ALLOWED_ORIGINS=https://your-frontend.onrender.com`
- [ ] `FRONTEND_BASE_URL=https://your-frontend.onrender.com`
- [ ] `EMAIL_HOST_USER=<your-email>`
- [ ] `EMAIL_HOST_PASSWORD=<app-password>`

### Frontend (.env)
- [ ] `VITE_API_BASE_URL=https://your-backend.onrender.com`
- [ ] `VITE_API_TIMEOUT=30000`

---

## 🐛 Common Issues & Solutions

### Backend won't start
```
Check:
1. requirements.txt has all dependencies
2. Procfile exists and is correctly formatted
3. Environment variables are set (especially DATABASE_URL)
4. Check build logs for errors
```

### "Cannot GET /api/users/"
```
Solution:
1. Ensure backend is running (check Logs tab)
2. Check CORS_ALLOWED_ORIGINS includes your frontend URL
3. Verify API endpoints exist in your urls.py
```

### Frontend can't reach backend
```
Solution:
1. Check VITE_API_BASE_URL is correct
2. Verify backend URL is accessible from browser
3. Check browser console for CORS errors
4. Backend CORS settings must allow frontend domain
```

### Static files not loading (CSS, JS broken)
```
Solution:
1. Run: python manage.py collectstatic --noinput
2. Ensure STATIC_ROOT and STATICFILES_STORAGE are set in settings.py
3. Check WhiteNoise is in MIDDLEWARE
```

### Database errors
```
Solution:
1. Verify DATABASE_URL is correct
2. Run migrations: python manage.py migrate
3. Check PostgreSQL is running on Render
4. Use `dj-database-url` for URL parsing
```

---

## 📞 Support

If you encounter issues:
1. Check the **Logs** tab in Render Dashboard
2. Review the **RENDER_DEPLOYMENT_GUIDE.md** for detailed info
3. Look for specific error messages in logs
4. Verify all environment variables are set

---

## 🔄 Redeploying After Changes

### For Backend:
```bash
git add .
git commit -m "Backend updates"
git push origin main
# Render will auto-deploy
```

### For Frontend:
```bash
git add .
git commit -m "Frontend updates"
git push origin main
# Render will auto-deploy
```

---

## 💾 Backup Your Database

```bash
# Connect to PostgreSQL and backup
pg_dump <DATABASE_URL> > backup.sql

# Restore if needed
psql <DATABASE_URL> < backup.sql
```

---

Happy Deploying! 🎉
