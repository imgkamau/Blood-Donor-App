# Railway Postgres Migration Guide

## Overview
This guide will help you migrate from AWS RDS to Railway Postgres for your Blood Donor App backend.

## Step 1: Add Postgres Database to Railway

1. **Go to your Railway project dashboard**
2. **Click "New" → "Database" → "PostgreSQL"**
3. **Railway will automatically:**
   - Create a new Postgres database
   - Generate connection credentials
   - Add the `DATABASE_URL` environment variable to your backend service

## Step 2: Verify Environment Variables

After adding the database, check that Railway has added these environment variables to your backend service:

- `DATABASE_URL` - The complete connection string
- `PGHOST` - Database host
- `PGPORT` - Database port
- `PGUSER` - Database username
- `PGPASSWORD` - Database password
- `PGDATABASE` - Database name

## Step 3: Setup Database Schema

1. **Deploy the updated backend** (Railway will auto-deploy from GitHub)
2. **Run the database setup script** in Railway's console:

```bash
# In Railway's console for your backend service
python setup_railway_db.py
```

This script will:
- Create the `donate` schema
- Create the `blood` table with proper indexes
- Add geospatial indexes for location queries
- Create triggers for `updated_at` timestamps
- Insert test data

## Step 4: Test the Migration

### Test Database Connection
```bash
# Test the connection
python -c "
import os
from sqlalchemy import create_engine
engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    result = conn.execute('SELECT version()')
    print('PostgreSQL version:', result.fetchone()[0])
"
```

### Test API Endpoints
```bash
# Health check
curl https://blood-donor-app-production-aa1d.up.railway.app/api/v1/health

# Create a donor
curl -X POST "https://blood-donor-app-production-aa1d.up.railway.app/api/v1/donors" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "phone_number": "+254712345678",
    "blood_type": "O+",
    "latitude": -1.286389,
    "longitude": 36.817223,
    "city": "Nairobi"
  }'

# Search donors
curl -X POST "https://blood-donor-app-production-aa1d.up.railway.app/api/v1/donors/search" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": -1.286389,
    "longitude": 36.817223,
    "radius_km": 10,
    "blood_type": "O+"
  }'
```

## Step 5: Update Flutter App (if needed)

Your Flutter app should continue working without changes since the API endpoints remain the same. The only change is the database backend.

## Benefits of Railway Postgres

1. **Simplified Infrastructure**: Everything in one platform
2. **Automatic Backups**: Railway handles backups automatically
3. **Easy Scaling**: Scale database and backend together
4. **Cost Effective**: No separate AWS RDS costs
5. **Better Integration**: Seamless connection between services

## Troubleshooting

### Database Connection Issues
- Check that `DATABASE_URL` is set in Railway environment variables
- Verify the database service is running
- Check Railway logs for connection errors

### Schema Issues
- Run `setup_railway_db.py` again if schema creation failed
- Check Railway logs for SQL errors
- Verify database permissions

### API Issues
- Check backend service logs in Railway
- Verify CORS settings
- Test endpoints individually

## Migration Checklist

- [ ] Add Postgres database to Railway project
- [ ] Verify `DATABASE_URL` environment variable
- [ ] Deploy updated backend code
- [ ] Run database setup script
- [ ] Test database connection
- [ ] Test API endpoints
- [ ] Verify Flutter app still works
- [ ] Monitor Railway logs for any issues

## Next Steps

1. **Monitor Performance**: Check Railway metrics for database performance
2. **Set up Monitoring**: Consider adding database monitoring
3. **Backup Strategy**: Verify Railway's automatic backups
4. **Cost Optimization**: Monitor usage and optimize if needed

## Support

If you encounter any issues:
1. Check Railway logs first
2. Verify environment variables
3. Test database connection manually
4. Check API endpoint responses
