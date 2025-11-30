# Deployment Guide: Render.com

This guide will help you deploy both the Django backend and React frontend to Render.com.

## Prerequisites
- A Render.com account (free or paid)
- GitHub repository with your code pushed
- PostgreSQL database on Render (for backend)

---

## Part 1: Backend Deployment (Django)

### Step 1: Prepare Django for Production

1. **Update your `.env` file** - Use the values from `.env.example`:
   ```
   DEBUG=False
   SECRET_KEY=generate_a_secure_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/student_tracking
   ALLOWED_HOSTS=your-backend.onrender.com,localhost
   CORS_ALLOWED_ORIGINS=https://your-frontend.onrender.com
   FRONTEND_BASE_URL=https://your-frontend.onrender.com
   ```

2. **Generate a secure SECRET_KEY**:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

3. **Update `backend/settings.py`** to use environment variables:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   DEBUG = os.getenv('DEBUG', 'False') == 'True'
   SECRET_KEY = os.getenv('SECRET_KEY')
   ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
   DATABASES = {
       'default': dj_database_url.config(
           default=os.getenv('DATABASE_URL'),
           conn_max_age=600
       )
   }
   CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
   FRONTEND_BASE_URL = os.getenv('FRONTEND_BASE_URL')
   ```

### Step 2: Add Required Dependencies

Update your `requirements.txt`:
```bash
Django==5.2.8
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.2
django-cors-headers==4.3.1
python-dotenv==1.0.0
dj-database-url==2.1.0
gunicorn==21.2.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
Pillow==10.1.0
```

Generate requirements.txt:
```bash
pip freeze > requirements.txt
```

### Step 3: Create `Procfile` in Backend Root

Create a file named `Procfile` (no extension) in the backend directory:
```
release: python manage.py migrate
web: gunicorn backend.wsgi:application
```

### Step 4: Update Settings for Static Files

Add to `backend/settings.py`:
```python
import os
from pathlib import Path

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security headers for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_SECURITY_POLICY = {
        'default-src': ("'self'",),
    }
    X_FRAME_OPTIONS = 'DENY'
```

### Step 5: Create on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `student-tracking-backend`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn backend.wsgi:application
     ```
   - **Plan**: Free or Paid (depending on your needs)

5. Add **Environment Variables**:
   - `DEBUG`: `False`
   - `SECRET_KEY`: (paste your generated key)
   - `DATABASE_URL`: (PostgreSQL URL from Render)
   - `ALLOWED_HOSTS`: `student-tracking-backend.onrender.com`
   - `CORS_ALLOWED_ORIGINS`: `https://student-tracking-frontend.onrender.com`
   - `FRONTEND_BASE_URL`: `https://student-tracking-frontend.onrender.com`
   - `EMAIL_HOST_USER`: (your Gmail)
   - `EMAIL_HOST_PASSWORD`: (Gmail app password)

6. Click **"Create Web Service"**

### Step 6: Create PostgreSQL Database

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `student-tracking-db`
   - **Database**: `student_tracking`
   - **Plan**: Free or Paid

3. Copy the `External Database URL` and use it as `DATABASE_URL` environment variable

---

## Part 2: Frontend Deployment (React)

### Step 1: Configure Environment Variables

Create `.env` in the frontend root (or update `.env.example`):
```
VITE_API_BASE_URL=https://student-tracking-backend.onrender.com
VITE_API_TIMEOUT=30000
```

### Step 2: Update `src/api.js`

Ensure your API configuration uses environment variables:
```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: import.meta.env.VITE_API_TIMEOUT || 30000,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### Step 3: Create `render.yaml` (Optional but Recommended)

In the root directory, create `render.yaml`:
```yaml
services:
  - type: web
    name: student-tracking-frontend
    env: static
    buildCommand: npm install && npm run build
    staticPublishPath: dist
    envVars:
      - key: VITE_API_BASE_URL
        value: https://student-tracking-backend.onrender.com
```

### Step 4: Deploy Frontend on Render

1. In Render Dashboard, click **"New +"** → **"Static Site"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `student-tracking-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Plan**: Free or Paid

4. Add **Environment Variables**:
   - `VITE_API_BASE_URL`: `https://student-tracking-backend.onrender.com`

5. Click **"Create Static Site"**

---

## Part 3: Final Configuration

### Backend Routes Update
Ensure your backend URLs include the full path:
```python
# backend/urls.py
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/students/', include('students.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### Test the Deployment

1. Wait for both services to deploy (5-10 minutes)
2. Test backend: `https://student-tracking-backend.onrender.com/api/users/login/`
3. Test frontend: `https://student-tracking-frontend.onrender.com`
4. Check browser console for any API errors

---

## Troubleshooting

### Backend Issues
- **Build fails**: Check `requirements.txt` syntax and Python version
- **Database errors**: Ensure `DATABASE_URL` is set correctly
- **Static files missing**: Make sure `STATIC_ROOT` and `STATICFILES_STORAGE` are configured
- **CORS errors**: Check `CORS_ALLOWED_ORIGINS` matches your frontend URL

### Frontend Issues
- **API calls failing**: Verify `VITE_API_BASE_URL` is correct
- **Build fails**: Check `npm install` and `npm run build` locally first
- **Blank page**: Check browser console for errors

### Logs
- **View logs**: Render Dashboard → Service → "Logs" tab
- Monitor for errors and adjust environment variables as needed

---

## Additional Resources
- [Render Django Deployment](https://render.com/docs/deploy-django)
- [Render React Deployment](https://render.com/docs/deploy-react)
- [Django Production Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)

---

## Security Checklist

- ✅ `DEBUG=False` in production
- ✅ `SECRET_KEY` is unique and secure
- ✅ `ALLOWED_HOSTS` contains only your domain
- ✅ `CORS_ALLOWED_ORIGINS` is restricted
- ✅ Email credentials are in environment variables (not in code)
- ✅ Database credentials are in environment variables
- ✅ HTTPS is enforced
- ✅ Security headers are configured

---

## Deployment Diagram

```
GitHub Repository
    ↓
Render Dashboard
    ├─ Backend Service (Django + Gunicorn)
    │  ├─ Environment Variables
    │  └─ PostgreSQL Database
    │
    └─ Frontend Service (React + Vite)
       └─ Environment Variables
```

Happy deploying! 🚀
