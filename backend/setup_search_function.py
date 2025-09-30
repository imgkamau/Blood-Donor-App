#!/usr/bin/env python3
"""
Setup the search function in the database
"""

from sqlalchemy import create_engine, text

def setup_search_function():
    print("🔍 Setting up search function...")
    
    try:
        engine = create_engine("postgresql://postgres:123456@localhost:5432/blood_donor_db")
        
        with engine.connect() as conn:
            # Ensure UUID extension is available in public schema
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\" SCHEMA public;"))
            
            # Create the search function
            conn.execute(text("""
                -- Function to calculate distance between two points using Haversine formula (in km)
                CREATE OR REPLACE FUNCTION donate.calculate_distance_km(
                    lat1 DECIMAL, lon1 DECIMAL,
                    lat2 DECIMAL, lon2 DECIMAL
                )
                RETURNS DECIMAL AS $$
                DECLARE
                    R DECIMAL := 6371; -- Radius of Earth in kilometers
                    dLat DECIMAL := radians(lat2 - lat1);
                    dLon DECIMAL := radians(lon2 - lon1);
                    a DECIMAL;
                    c DECIMAL;
                    distance DECIMAL;
                BEGIN
                    a := sin(dLat / 2) * sin(dLat / 2) +
                         cos(radians(lat1)) * cos(radians(lat2)) *
                         sin(dLon / 2) * sin(dLon / 2);
                    c := 2 * atan2(sqrt(a), sqrt(1 - a));
                    distance := R * c;
                    RETURN distance;
                END;
                $$ LANGUAGE plpgsql IMMUTABLE;
            """))
            
            conn.execute(text("""
                -- Function to search for donors by blood type and proximity
                CREATE OR REPLACE FUNCTION donate.search_donors(
                    p_blood_type VARCHAR,
                    p_user_latitude DECIMAL,
                    p_user_longitude DECIMAL,
                    p_max_distance_km DECIMAL DEFAULT 50
                )
                RETURNS TABLE (
                    id UUID,
                    first_name VARCHAR,
                    phone_number VARCHAR,
                    blood_type VARCHAR,
                    latitude DECIMAL,
                    longitude DECIMAL,
                    address TEXT,
                    city VARCHAR,
                    country VARCHAR,
                    is_verified BOOLEAN,
                    is_available BOOLEAN,
                    last_donation_date DATE,
                    created_at TIMESTAMP WITH TIME ZONE,
                    updated_at TIMESTAMP WITH TIME ZONE,
                    distance_km DECIMAL
                ) AS $$
                BEGIN
                    RETURN QUERY
                    SELECT
                        b.id,
                        b.first_name,
                        b.phone_number,
                        b.blood_type,
                        b.latitude,
                        b.longitude,
                        b.address,
                        b.city,
                        b.country,
                        b.is_verified,
                        b.is_available,
                        b.last_donation_date,
                        b.created_at,
                        b.updated_at,
                        donate.calculate_distance_km(p_user_latitude, p_user_longitude, b.latitude, b.longitude) AS distance_km
                    FROM
                        donate.blood AS b
                    WHERE
                        b.blood_type = p_blood_type
                        AND b.is_available = TRUE
                        AND b.is_verified = TRUE
                        AND donate.calculate_distance_km(p_user_latitude, p_user_longitude, b.latitude, b.longitude) <= p_max_distance_km
                    ORDER BY
                        distance_km
                    LIMIT 20; -- Limit to 20 results to prevent abuse
                END;
                $$ LANGUAGE plpgsql;
            """))
            
            # Skip sample data for now - we'll add it through the API
            print("✅ Search function created successfully (sample data skipped)")
            
            conn.commit()
            
    except Exception as e:
        print(f"❌ Error setting up search function: {e}")

if __name__ == "__main__":
    setup_search_function()
