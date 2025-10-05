#!/usr/bin/env python3
"""
Script to create the search_logs table in Railway PostgreSQL.
Run this via Railway CLI: railway run python create_search_logs_table.py
"""

import os
import psycopg2

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:YriFkwdSDCFRreklJsMUZnXjJKJVusff@postgres.railway.internal:5432/railway"
)

def create_search_logs_table():
    """Create the search_logs table"""
    try:
        print("🔍 Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("📊 Creating search_logs table...")
        
        # Create the table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public.search_logs (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                blood_type VARCHAR(5) NOT NULL,
                latitude DECIMAL(10, 8) NOT NULL,
                longitude DECIMAL(11, 8) NOT NULL,
                radius_km DECIMAL(8, 2) NOT NULL,
                results_count INTEGER NOT NULL DEFAULT 0,
                client_ip VARCHAR(45),
                searched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("✅ Table 'public.search_logs' created")
        
        # Create indexes
        print("📑 Creating indexes...")
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_search_logs_searched_at 
            ON public.search_logs (searched_at DESC)
        """)
        conn.commit()
        print("✅ Index 'idx_search_logs_searched_at' created")
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_search_logs_blood_type 
            ON public.search_logs (blood_type)
        """)
        conn.commit()
        print("✅ Index 'idx_search_logs_blood_type' created")
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_search_logs_client_ip 
            ON public.search_logs (client_ip)
        """)
        conn.commit()
        print("✅ Index 'idx_search_logs_client_ip' created")
        
        # Verify table exists
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'search_logs'
        """)
        result = cursor.fetchone()
        
        if result[0] > 0:
            print("\n✅ SUCCESS! search_logs table is ready")
            
            # Check if there are any records
            cursor.execute("SELECT COUNT(*) FROM public.search_logs")
            count = cursor.fetchone()[0]
            print(f"📊 Current records in search_logs: {count}")
        else:
            print("\n⚠️  Warning: Table created but not found in schema")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    create_search_logs_table()

