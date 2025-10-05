# Fix Search Activity Logs

## Problem

The **Search Activity** page shows "0 of 0 searches" because the `search_logs` table doesn't exist in the database.

## Why It Happened

When the backend tried to create the database schema, it failed at the "unique constraint on phone_number" step (due to duplicate phone numbers). This caused the entire transaction to roll back, preventing the `search_logs` table from being created.

## Solution

Railway is now redeploying with a fix that:
1. ✅ Catches the unique constraint error
2. ✅ Rolls back only that step
3. ✅ Continues to create `search_logs` table
4. ✅ Creates all indexes

---

## What's Happening Now

**Railway is redeploying** (~2-3 minutes) with the fixed initialization logic.

Once deployed, the `search_logs` table will be created automatically on the next backend restart.

---

## After Railway Deploys

### Option 1: Wait for Next Backend Restart

The table will be created automatically on the next restart. You can trigger a restart in Railway:

1. Go to Railway Dashboard
2. Click your backend service
3. Click "Settings"
4. Scroll to "Danger Zone"
5. Click "Restart"

### Option 2: Run the Script Manually (If You Have Railway CLI)

```bash
# Make sure you're linked to the project
railway link

# Run the script to create the table
railway run python create_search_logs_table.py
```

This will:
- Connect to your Railway PostgreSQL database
- Create the `search_logs` table
- Create all required indexes
- Verify the table exists

---

## How to Verify It's Working

### 1. Check Railway Logs

After restart, you should see:
```
🔍 Checking database connection and schema...
✅ Connected to database: railway
✅ Extension uuid-ossp created
✅ Table 'public.blood' created
⚠️  Could not create unique constraint (likely duplicate phone numbers exist)
✅ Indexes created
✅ Table 'public.search_logs' created  ← This should appear now!
✅ Search logs indexes created
```

### 2. Test the Search Activity Page

1. Have someone use the Flutter app to search for blood donors
2. Go to admin portal: `blood-donor-app.vercel.app/admin/activity`
3. You should see search records appear

### 3. Check the Database Directly

In Railway's PostgreSQL console:
```sql
-- Check if table exists
SELECT COUNT(*) FROM public.search_logs;

-- View recent searches
SELECT * FROM public.search_logs ORDER BY searched_at DESC LIMIT 10;
```

---

## Future: Fix Duplicate Phone Numbers

The unique constraint couldn't be created because of duplicate phone numbers. 

**To fix this later:**

1. Run the cleanup script:
   ```bash
   railway run python fix_duplicate_phone_numbers.py
   ```

2. This will:
   - Find all duplicate phone numbers
   - Keep the most recent entry
   - Delete older duplicates
   - Allow the unique constraint to be created

3. Restart the backend to apply the unique constraint

---

## What the search_logs Table Does

**Purpose:** Tracks all blood donor searches made through the app

**Columns:**
- `id`: Unique identifier
- `blood_type`: Blood type searched (A+, O-, etc.)
- `latitude/longitude`: Search location
- `radius_km`: Search radius
- `results_count`: Number of donors found
- `client_ip`: IP address (for rate limiting)
- `searched_at`: Timestamp

**Uses:**
- Admin dashboard analytics
- Understanding search patterns
- Rate limiting abuse prevention
- Future: Heat maps of blood demand

---

## Summary

✅ **Railway is deploying the fix now**
✅ **search_logs table will be created on next restart**
✅ **Search Activity page will start working**
⚠️  **Duplicate phone numbers still need to be cleaned up (optional)**

**Next Step:** Wait ~3 minutes for Railway to deploy, then restart the backend service.

