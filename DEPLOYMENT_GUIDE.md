# Blood Donor App - Complete Deployment Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Blood Donor System                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Flutter App (Mobile)  →  Railway Backend (FastAPI)     │
│                            ↓                              │
│  Admin Portal (Vercel) →  Railway PostgreSQL Database   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Backend Deployment (Railway) ✅ DONE

Your backend is already deployed and running!

**URL:** `https://blood-donor-app-production-aa1d.up.railway.app`

**What's Running:**
- FastAPI backend
- PostgreSQL database
- Tables: `public.blood`, `public.search_logs`
- Security features: Phone masking, rate limiting
- Search logging for admin portal

**Status:** ✅ Live and auto-deploying from `main` branch

---

## 2. Frontend Deployment (Vercel) - TODO

### Step 1: Get Railway Database Public URL

1. Go to Railway dashboard
2. Click your PostgreSQL database
3. Go to **"Connect"** tab
4. Copy the **"Public Network"** connection string

It should look like:
```
postgresql://postgres:YriFkwdSDCFRreklJsMUZnXjJKJVusff@monorail.proxy.rlwy.net:12345/railway
```

**Important:** Use the PUBLIC URL (monorail.proxy.rlwy.net), NOT the internal one (postgres.railway.internal)

### Step 2: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repository: `imgkamau/Blood-Donor-App`
4. **IMPORTANT:** Set **Root Directory** to `frontend`
5. Click **"Environment Variables"**
6. Add these variables:

```
DATABASE_URL = postgresql://postgres:YriFkwdSDCFRreklJsMUZnXjJKJVusff@monorail.proxy.rlwy.net:XXXXX/railway
ADMIN_PASSWORD = admin123
```

7. Click **"Deploy"**

### Step 3: Wait for Build

- Build takes ~2-3 minutes
- Vercel will automatically detect Next.js configuration
- After deployment, you'll get a URL like: `your-project.vercel.app`

### Step 4: Access Admin Portal

1. Go to `your-project.vercel.app/admin`
2. Enter password: `admin123` (or your custom password)
3. View dashboard with real-time data from Railway database

---

## 3. Flutter App - Current Status

Your Flutter app is already configured to use the Railway backend.

**Backend URL:** `https://blood-donor-app-production-aa1d.up.railway.app/api/v1`

**Features Working:**
- ✅ Donor enrollment
- ✅ Blood search (with phone masking)
- ✅ Rate limiting (5 searches/hour)
- ✅ Search logging (visible in admin portal)

**To build new APK with latest changes:**
```bash
cd android
flutter clean
flutter pub get
flutter build appbundle --release
```

---

## 4. What You Have Now

### Backend (Railway)
- ✅ FastAPI REST API
- ✅ PostgreSQL database with 2 tables
- ✅ Security: Phone masking, rate limiting, result limits
- ✅ Search activity logging
- ✅ WebSocket support (for real-time updates)
- ✅ Auto-deploys from `main` branch

### Frontend (Vercel - To Deploy)
- 📊 Dashboard with donor statistics
- 👥 Donor management (view, search, filter)
- 🔍 Search activity logs
- 📱 Responsive design
- 🔐 Password-protected

### Mobile App (Flutter)
- ✅ Donor enrollment
- ✅ Blood search
- ✅ Real-time updates via WebSocket
- ✅ Terms & Conditions
- ✅ Privacy-focused (masked phone numbers)

---

## 5. Environment Variables Summary

### Railway (Backend)
```env
DATABASE_URL=postgresql://postgres:password@postgres.railway.internal:5432/railway
```
*(Auto-configured by Railway)*

### Vercel (Frontend)
```env
DATABASE_URL=postgresql://postgres:password@monorail.proxy.rlwy.net:XXXXX/railway
ADMIN_PASSWORD=admin123
```

### Flutter App
```dart
// lib/config/api_config.dart
static const String baseUrl = 'https://blood-donor-app-production-aa1d.up.railway.app/api/v1';
```

---

## 6. Post-Deployment Checklist

After deploying to Vercel:

- [ ] Test admin login
- [ ] Verify dashboard shows correct donor count
- [ ] Check donors list loads
- [ ] Verify search activity logs appear
- [ ] Test filtering by blood type
- [ ] Confirm phone numbers are displayed (admins see full numbers)
- [ ] Check that new donor enrollments appear in real-time

---

## 7. Monitoring & Maintenance

### Railway Backend
- **Logs:** Railway dashboard → Your service → Logs
- **Database:** Railway dashboard → PostgreSQL → Data tab
- **Metrics:** Railway dashboard → Metrics

### Vercel Frontend
- **Logs:** Vercel dashboard → Your project → Logs
- **Analytics:** Vercel dashboard → Analytics
- **Deployments:** Vercel dashboard → Deployments

### Flutter App
- **Crash reports:** Google Play Console → Quality
- **User feedback:** Google Play Console → Reviews

---

## 8. Costs

### Railway
- **Free Tier:** $5 credit/month
- **Your Usage:** Backend + PostgreSQL
- **Estimate:** Free tier should be sufficient for testing

### Vercel
- **Free Tier:** Unlimited deployments
- **Your Usage:** Next.js frontend
- **Estimate:** Free tier is sufficient

**Total Cost:** $0/month (within free tiers)

---

## 9. Scaling Considerations

When you outgrow free tiers:

### Railway Pro ($5/month + usage)
- More execution hours
- Better performance
- Multiple environments

### Vercel Pro ($20/month)
- Custom domains
- Advanced analytics
- Team collaboration

---

## 10. Troubleshooting

### Frontend can't connect to database
- Verify you're using PUBLIC Railway URL (not internal)
- Check environment variables are set in Vercel
- Redeploy after adding variables

### Admin portal shows empty data
- Confirm database tables exist in Railway
- Check Railway backend logs for errors
- Verify `search_logs` table was created

### Build fails on Vercel
- Ensure root directory is set to `frontend`
- Check package.json has all dependencies
- Run `cd frontend && npm install` locally first

---

## 11. Next Steps

1. ✅ **Deploy frontend to Vercel** (follow Step 2 above)
2. 🔐 **Change admin password** from default `admin123`
3. 📱 **Build new Flutter APK** with latest backend
4. 🚀 **Test entire system** end-to-end
5. 📊 **Monitor usage** in first few days
6. 🎯 **Add custom domain** (optional, Vercel Pro)

---

## 12. Support

- **Backend Issues:** Check Railway logs
- **Frontend Issues:** Check Vercel logs
- **Database Issues:** Check Railway PostgreSQL data tab
- **Flutter App Issues:** Check device logcat

---

## Summary

You now have a **complete, production-ready system**:

- ✅ Secure backend with rate limiting
- ✅ Admin portal for monitoring
- ✅ Mobile app for users
- ✅ Real-time updates
- ✅ Privacy-focused design
- ✅ Zero management required

**All that's left:** Deploy the frontend to Vercel (5 minutes) and you're live!
