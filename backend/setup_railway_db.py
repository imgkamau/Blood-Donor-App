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
            
            # Create schema and table (matching RDS schema)
            schema_sql = """
            -- Create schema if not exists
            CREATE SCHEMA IF NOT EXISTS donate;
            
            -- Set the search path to include the donate schema
            SET search_path TO donate, public;
            
            -- Create uuid-ossp extension in public schema (if not exists)
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
            
            -- Create the blood table in the donate schema (matching RDS)
            CREATE TABLE IF NOT EXISTS donate.blood (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                donor_id UUID,
                first_name VARCHAR(100) NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                blood_type VARCHAR(5) NOT NULL CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
                latitude DECIMAL(10, 8) NOT NULL,
                longitude DECIMAL(11, 8) NOT NULL,
                address TEXT,
                city VARCHAR(100),
                country VARCHAR(100) DEFAULT 'Kenya',
                is_verified BOOLEAN DEFAULT FALSE,
                is_available BOOLEAN DEFAULT TRUE,
                last_donation_date DATE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Create indexes for better performance (matching RDS)
            CREATE INDEX IF NOT EXISTS idx_blood_blood_type ON donate.blood(blood_type);
            CREATE INDEX IF NOT EXISTS idx_blood_latitude ON donate.blood(latitude);
            CREATE INDEX IF NOT EXISTS idx_blood_longitude ON donate.blood(longitude);
            CREATE INDEX IF NOT EXISTS idx_blood_available ON donate.blood(is_available);
            CREATE INDEX IF NOT EXISTS idx_blood_city ON donate.blood(city);
            CREATE INDEX IF NOT EXISTS idx_blood_created_at ON donate.blood(created_at);
            
            -- Create function to update updated_at timestamp
            CREATE OR REPLACE FUNCTION donate.update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
            
            -- Create trigger to automatically update updated_at
            CREATE TRIGGER update_blood_updated_at 
                BEFORE UPDATE ON donate.blood
                FOR EACH ROW
                EXECUTE FUNCTION donate.update_updated_at_column();
            """
            
            # Execute schema creation
            conn.execute(text(schema_sql))
            conn.commit()
            
            print("✅ Database schema created successfully!")
            print("✅ Table 'donate.blood' created with indexes")
            print("✅ Triggers and functions created")
            
            # Test insert (matching RDS schema)
            test_donor = {
                'first_name': 'Test',
                'phone_number': '+254700000000',
                'blood_type': 'O+',
                'latitude': -1.286389,
                'longitude': 36.817223,
                'city': 'Nairobi',
                'country': 'Kenya',
                'is_verified': False,
                'is_available': True
            }
            
            insert_sql = """
            INSERT INTO donate.blood 
            (first_name, phone_number, blood_type, latitude, longitude, city, country, is_verified, is_available)
            VALUES (:first_name, :phone_number, :blood_type, :latitude, :longitude, :city, :country, :is_verified, :is_available)
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
