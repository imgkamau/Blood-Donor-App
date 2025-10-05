import os
import psycopg2

# Connect to Railway database
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()

# Update all donors to verified
cur.execute('UPDATE public.blood SET is_verified = TRUE')
conn.commit()

# Check how many donors are now verified
cur.execute('SELECT COUNT(*) FROM public.blood WHERE is_verified = TRUE')
count = cur.fetchone()[0]
print(f'✅ Updated {count} donors to verified status')

conn.close()

