# Vercel Environment Variables Setup

## Required Environment Variables

Your Vercel admin portal needs these environment variables to connect to the Railway database.

### 1. Get Railway PostgreSQL Public URL

1. Go to **Railway Dashboard**: https://railway.app
2. Open your **Blood Donor App** project
3. Click on the **PostgreSQL** service (elephant icon)
4. Click the **"Connect"** tab
5. Look for **"Public Network"** section
6. Copy the connection string (looks like):
   ```
   postgresql://postgres:YriFkwdSDCFRreklJsMUZnXjJKJVusff@monorail.proxy.rlwy.net:12345/railway
   ```

**IMPORTANT:** Use the **PUBLIC** URL (monorail.proxy.rlwy.net), NOT the internal URL (postgres.railway.internal)

---

### 2. Add to Vercel

1. Go to **Vercel Dashboard**: https://vercel.com
2. Click your **blood-donor-app** project
3. Go to **Settings** → **Environment Variables**
4. Add these variables:

#### Variable 1: DATABASE_URL
```
Name: DATABASE_URL
Value: postgresql://postgres:YriFkwdSDCFRreklJsMUZnXjJKJVusff@monorail.proxy.rlwy.net:XXXXX/railway
Environment: Production, Preview, Development (select all)
```

#### Variable 2: ADMIN_PASSWORD (Optional - already hardcoded)
```
Name: ADMIN_PASSWORD
Value: admin123
Environment: Production, Preview, Development (select all)
```

---

### 3. Redeploy

After adding environment variables:

1. Go to **Deployments** tab in Vercel
2. Click the **three dots** (...) on the latest deployment
3. Click **"Redeploy"**

OR

Vercel will automatically redeploy on the next Git push.

---

### 4. Test Connection

Once redeployed:
1. Go to `blood-donor-app.vercel.app/admin`
2. Login with `admin123`
3. Dashboard should load with live data from Railway PostgreSQL

---

## Troubleshooting

### If you still get ECONNRESET:

1. **Check Railway database is running:**
   - Railway Dashboard → PostgreSQL service → Should show "Active"

2. **Verify PUBLIC URL is used:**
   - Should start with `monorail.proxy.rlwy.net`
   - NOT `postgres.railway.internal` (internal only works within Railway)

3. **Check Railway database allows external connections:**
   - Railway PostgreSQL allows public connections by default on paid plans
   - Free tier may have limitations

4. **Test connection locally:**
   ```bash
   cd frontend
   # Create .env.local
   echo "DATABASE_URL=postgresql://..." > .env.local
   npm run dev
   # Visit http://localhost:3000/admin
   ```

---

## Current Status

✅ Frontend deployed to Vercel
✅ Backend deployed to Railway
✅ Authentication working
❌ Database connection failing (missing env var)

**Next Step:** Add DATABASE_URL to Vercel environment variables

