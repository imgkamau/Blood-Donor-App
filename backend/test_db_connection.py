#!/usr/bin/env python3
"""
Test database connection and setup
"""

import psycopg2
from sqlalchemy import create_engine, text
import os

def test_database_connection():
    print("🔍 Testing Database Connection...")
    print("-" * 50)
    
    # Test direct psycopg2 connection
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="123456",
            database="postgres"
        )
        print("✅ Direct psycopg2 connection: SUCCESS")
        
        # Test if we can create the database
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if blood_donor_db exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'blood_donor_db'")
        if cursor.fetchone():
            print("✅ Database 'blood_donor_db' exists")
        else:
            print("❌ Database 'blood_donor_db' does not exist")
            print("   Creating database...")
            cursor.execute("CREATE DATABASE blood_donor_db")
            print("✅ Database 'blood_donor_db' created")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Direct psycopg2 connection: FAILED - {e}")
        return False
    
    # Test SQLAlchemy connection to the specific database
    try:
        engine = create_engine("postgresql://postgres:123456@localhost:5432/blood_donor_db")
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ SQLAlchemy connection to blood_donor_db: SUCCESS")
        
        # Test schema creation
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS donate"))
            conn.execute(text("SET search_path TO donate, public"))
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
            conn.commit()
        print("✅ Schema and extension setup: SUCCESS")
        
    except Exception as e:
        print(f"❌ SQLAlchemy connection: FAILED - {e}")
        return False
    
    print("-" * 50)
    print("🎉 Database setup completed successfully!")
    return True

if __name__ == "__main__":
    test_database_connection()
