# Quick Start: Set Your Admin Password

## Immediate Steps (Do This Now!)

### 1. Go to Vercel Dashboard
Visit: https://vercel.com/dashboard

### 2. Open Your Project
Click on **blood-donor-app**

### 3. Add Environment Variable
1. Click **Settings** (top navigation)
2. Click **Environment Variables** (left sidebar)
3. Click **Add New**
4. Fill in:
   ```
   Name: ADMIN_PASSWORD
   Value: [Choose a strong password - see suggestions below]
   ```
5. Check all environments: ✅ Production ✅ Preview ✅ Development
6. Click **Save**

### 4. Redeploy
1. Go to **Deployments** tab
2. Click the **three dots** (...) on the latest deployment
3. Click **"Redeploy"**
4. Wait ~2 minutes

### 5. Test Login
1. Visit: `blood-donor-app.vercel.app/admin`
2. Enter your new password
3. You should see the dashboard

---

## Password Suggestions

Choose one (or create your own):

- `BloodDonor2024!Kenya`
- `K3nya$Bl00d#Adm1n`
- `D0n0r_P0rt@l!2024`
- `Secure#BloodApp24`

**Requirements:**
- At least 12 characters
- Mix of uppercase/lowercase
- Include numbers and symbols

---

## What Changed

✅ **Before:** Password was `admin123` (visible on login page)
✅ **After:** Password is stored securely in Vercel environment variables
✅ **Security:** Password is never visible in code or UI

---

## If You Forget the Password

1. Go to Vercel → Settings → Environment Variables
2. Edit `ADMIN_PASSWORD`
3. Set a new password
4. Redeploy

---

## Default Password (Temporary)

Until you set `ADMIN_PASSWORD` in Vercel:
- **Temporary password:** `change-me-in-production`

**This works but is intentionally weak to remind you to change it!**

---

## Need Help?

See the full guide: `ADMIN_PASSWORD_SETUP.md`

