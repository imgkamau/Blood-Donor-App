#!/usr/bin/env python3
"""
Setup database schema for Railway Postgres
"""

import os
import psycopg2
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_railway_database():
    """Setup database schema for Railway Postgres"""
    print("🚀 Setting up Railway Postgres Database...")
    print("-" * 50)
    
    # Get DATABASE_URL from environment (Railway will provide this)
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not found!")
        print("   Make sure Railway has added the Postgres database to your project.")
        return False
    
    print(f"✅ DATABASE_URL found: {database_url[:50]}...")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            print("✅ Database connection: SUCCESS")
            
            # Create schema and table
            schema_sql = """
            -- Create schema if not exists
            CREATE SCHEMA IF NOT EXISTS donate;
            
            -- Create blood_donors table
            CREATE TABLE IF NOT EXISTS donate.blood (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100),
                phone_number VARCHAR(20) UNIQUE NOT NULL,
                blood_type VARCHAR(5) NOT NULL,
                latitude DECIMAL(10, 8) NOT NULL,
                longitude DECIMAL(11, 8) NOT NULL,
                city VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Create index for geospatial queries
            CREATE INDEX IF NOT EXISTS idx_blood_location 
            ON donate.blood USING GIST (ll_to_earth(latitude, longitude));
            
            -- Create index for blood type
            CREATE INDEX IF NOT EXISTS idx_blood_type 
            ON donate.blood (blood_type);
            
            -- Create index for city
            CREATE INDEX IF NOT EXISTS idx_blood_city 
            ON donate.blood (city);
            
            -- Add trigger for updated_at
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
            
            DROP TRIGGER IF EXISTS update_blood_updated_at ON donate.blood;
            CREATE TRIGGER update_blood_updated_at
                BEFORE UPDATE ON donate.blood
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
            """
            
            # Execute schema creation
            conn.execute(text(schema_sql))
            conn.commit()
            
            print("✅ Database schema created successfully!")
            print("✅ Table 'donate.blood' created with indexes")
            print("✅ Triggers and functions created")
            
            # Test insert
            test_donor = {
                'first_name': 'Test',
                'last_name': 'User',
                'phone_number': '+254700000000',
                'blood_type': 'O+',
                'latitude': -1.286389,
                'longitude': 36.817223,
                'city': 'Nairobi'
            }
            
            insert_sql = """
            INSERT INTO donate.blood 
            (first_name, last_name, phone_number, blood_type, latitude, longitude, city)
            VALUES (:first_name, :last_name, :phone_number, :blood_type, :latitude, :longitude, :city)
            ON CONFLICT (phone_number) DO NOTHING
            """
            
            conn.execute(text(insert_sql), test_donor)
            conn.commit()
            
            print("✅ Test data inserted successfully!")
            
            # Verify table structure
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_schema = 'donate' AND table_name = 'blood'
                ORDER BY ordinal_position
            """))
            
            print("\n📋 Table Structure:")
            print("-" * 30)
            for row in result:
                print(f"  {row[0]:<15} {row[1]:<15} {row[2]}")
            
            print("\n🎉 Railway Postgres setup completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    setup_railway_database()
