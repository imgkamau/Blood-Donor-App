-- Blood Donor App Database Schema Creation (Simple Version)
-- Run this script in pgAdmin to create the schema and tables

-- Create the 'donate' schema
CREATE SCHEMA IF NOT EXISTS donate;

-- Create uuid-ossp extension in public schema (if not exists)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set the search path to include the donate schema
SET search_path TO donate, public;

-- Create the blood table in the donate schema
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

-- Create indexes for better performance
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

-- Insert sample data for testing
INSERT INTO donate.blood (id, first_name, phone_number, blood_type, latitude, longitude, city, is_verified, is_available) VALUES
    ('550e8400-e29b-41d4-a716-446655440001', 'John', '+254712345678', 'O+', -1.286389, 36.817223, 'Nairobi', true, true),
    ('550e8400-e29b-41d4-a716-446655440002', 'Mary', '+254723456789', 'A+', -1.286389, 36.817223, 'Nairobi', true, true),
    ('550e8400-e29b-41d4-a716-446655440003', 'Peter', '+254734567890', 'B+', -4.043740, 39.668206, 'Mombasa', false, true),
    ('550e8400-e29b-41d4-a716-446655440004', 'Sarah', '+254745678901', 'AB+', -1.286389, 36.817223, 'Nairobi', true, true),
    ('550e8400-e29b-41d4-a716-446655440005', 'David', '+254756789012', 'O-', -0.023559, 35.302722, 'Kisumu', true, true),
    ('550e8400-e29b-41d4-a716-446655440006', 'Grace', '+254767890123', 'A-', -1.286389, 36.817223, 'Nairobi', false, true),
    ('550e8400-e29b-41d4-a716-446655440007', 'James', '+254778901234', 'B-', -4.043740, 39.668206, 'Mombasa', true, true),
    ('550e8400-e29b-41d4-a716-446655440008', 'Linda', '+254789012345', 'AB-', -1.286389, 36.817223, 'Nairobi', true, true)
ON CONFLICT (id) DO NOTHING;

-- Create a view for easy querying
CREATE OR REPLACE VIEW donate.blood_donors_view AS
SELECT 
    id,
    first_name,
    phone_number,
    blood_type,
    latitude,
    longitude,
    city,
    is_verified,
    is_available,
    created_at,
    updated_at
FROM donate.blood
WHERE is_available = true;

-- Create a function to calculate distance between two points (Haversine formula)
CREATE OR REPLACE FUNCTION donate.calculate_distance(
    lat1 DECIMAL,
    lon1 DECIMAL,
    lat2 DECIMAL,
    lon2 DECIMAL
)
RETURNS DECIMAL AS $$
DECLARE
    earth_radius DECIMAL := 6371; -- Earth's radius in kilometers
    dlat DECIMAL;
    dlon DECIMAL;
    a DECIMAL;
    c DECIMAL;
BEGIN
    dlat := radians(lat2 - lat1);
    dlon := radians(lon2 - lon1);
    
    a := sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2);
    c := 2 * atan2(sqrt(a), sqrt(1-a));
    
    RETURN earth_radius * c;
END;
$$ LANGUAGE plpgsql;

-- Create a function to search donors by blood type and location
CREATE OR REPLACE FUNCTION donate.search_donors(
    p_blood_type VARCHAR(5),
    p_latitude DECIMAL,
    p_longitude DECIMAL,
    p_radius_km DECIMAL DEFAULT 50
)
RETURNS TABLE (
    id UUID,
    first_name VARCHAR(100),
    phone_number VARCHAR(20),
    blood_type VARCHAR(5),
    city VARCHAR(100),
    is_verified BOOLEAN,
    distance_km DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        b.id,
        b.first_name,
        b.phone_number,
        b.blood_type,
        b.city,
        b.is_verified,
        ROUND(donate.calculate_distance(p_latitude, p_longitude, b.latitude, b.longitude), 2) as distance_km
    FROM donate.blood b
    WHERE b.blood_type = p_blood_type
        AND b.is_available = true
        AND donate.calculate_distance(p_latitude, p_longitude, b.latitude, b.longitude) <= p_radius_km
    ORDER BY distance_km ASC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- Display success message
DO $$
BEGIN
    RAISE NOTICE 'Blood Donor App database schema created successfully!';
    RAISE NOTICE 'Schema: donate';
    RAISE NOTICE 'Table: blood';
    RAISE NOTICE 'Sample data: 8 donors inserted';
    RAISE NOTICE 'View: blood_donors_view';
    RAISE NOTICE 'Function: search_donors()';
    RAISE NOTICE 'Ready to use!';
END $$;
